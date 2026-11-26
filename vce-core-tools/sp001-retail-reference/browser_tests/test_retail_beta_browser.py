"""SIMULATED two-session beta through real loopback HTTP, Chromium."""
import os
from pathlib import Path
import socket
from threading import Thread
import time

import pytest
import uvicorn
from playwright.sync_api import sync_playwright, expect
from test_retail_beta_inspection import beta
from test_retail_report_jwt_composition import keys
from test_inspection_observation_capture_browser import fill, candidate, save
from sp001.infrastructure.retail_beta_inspection import verify_export


def test_simulated_inspector_capture_supervisor_export(beta, tmp_path):
    _, app, token, _, _ = beta
    listener=socket.socket();listener.bind(('127.0.0.1',0));listener.listen(32)
    origin='http://127.0.0.1:'+str(listener.getsockname()[1])
    server=uvicorn.Server(uvicorn.Config(app,access_log=False,log_level='warning',lifespan='off'))
    thread=Thread(target=lambda:server.run(sockets=[listener]),daemon=True);thread.start()
    try:
        deadline=time.monotonic()+10
        while not server.started:
            assert thread.is_alive() and time.monotonic()<deadline
            time.sleep(.02)
        with sync_playwright() as p:
            options={'executable_path':os.environ['SP001_TEST_CHROMIUM']} if os.environ.get('SP001_TEST_CHROMIUM') else {}
            browser=p.chromium.launch(**options)
            inspector=browser.new_context(viewport={'width':390,'height':844})
            supervisor=browser.new_context()
            try:
                page=inspector.new_page();page.goto(origin+'/inspection-observations/capture')
                fill(page,candidate());page.locator('#request_id').fill('REQUEST')
                # Locate the existing upload input; photo preservation belongs to its existing tests.
                from PIL import Image
                photo=tmp_path/'photo.png';Image.new('RGB',(8,8),'blue').save(photo)
                page.locator('input[type=file]').set_input_files(photo)
                save(page,token('INSPECTOR'))
                expect(page.locator('#status')).to_contain_text('Guardado confirmado')
                page.goto(origin+'/retail-beta')
                page.locator('#token').fill(token('INSPECTOR'));page.locator('#load').click()
                expect(page.locator('#status')).to_contain_text('Expediente recuperado')
                page.locator('#request').fill('REQUEST')
                fields=page.locator('#outcomes fieldset')
                fields.nth(0).locator('select').select_option('NON_CONFORMANT')
                fields.nth(0).locator('textarea').fill('Foto de prueba: discrepancia declarada')
                fields.nth(1).locator('select').select_option('INSUFFICIENT_EVIDENCE')
                fields.nth(1).locator('textarea').fill('Parte posterior no visible')
                page.locator('#token').fill(token('INSPECTOR'));page.locator('#submit').click()
                expect(page.locator('#status')).to_contain_text('Revisión del inspector registrada')
                expect(page.locator('#submit')).to_be_disabled()
                expect(page.locator('#dossier')).to_contain_text('INSUFFICIENT_EVIDENCE')
                expect(page.locator('#outcomes select').nth(1)).to_have_value('INSUFFICIENT_EVIDENCE')
                expect(page.locator('#outcomes select').nth(1)).to_be_disabled()
                # A failed refresh preserves the registered outcomes and explains rejection.
                page.locator('#token').fill('invalid-token');page.locator('#load').click()
                expect(page.locator('#status')).to_contain_text('Credencial rechazada o vencida')
                expect(page.locator('#outcomes select').nth(1)).to_have_value('INSUFFICIENT_EVIDENCE')
                expect(page.locator('#action-status')).to_contain_text('Credencial rechazada o vencida')
                review=supervisor.new_page();review.goto(origin+'/retail-beta')
                review.locator('#token').fill(token('SUPERVISOR'));review.locator('#load').click()
                expect(review.locator('#dossier')).to_contain_text('INSUFFICIENT_EVIDENCE')
                review.locator('#token').fill(token('SUPERVISOR'));review.locator('#photo').click()
                expect(review.locator('#photo-preview')).to_be_visible()
                expect(review.locator('#status')).to_contain_text('Foto recuperada')
                review.locator('#rationale').fill('Requiere visita posterior y corrección')
                review.locator('#token').fill(token('SUPERVISOR'));review.locator('#decide').click()
                expect(review.locator('#status')).to_contain_text('Decisión registrada')
                review.reload();review.locator('#token').fill(token('SUPERVISOR'));review.locator('#load').click()
                expect(review.locator('#dossier')).to_contain_text('FOLLOW_UP_REQUIRED')
                review.locator('#token').fill(token('SUPERVISOR'))
                with review.expect_download() as pending:review.locator('#export').click()
                dossier=verify_export(Path(pending.value.path()).read_bytes())
                assert dossier['assignment']['simulated'] is True
                assert dossier['decision']['action']=='FOLLOW_UP_REQUIRED'
                assert page.evaluate('localStorage.length + sessionStorage.length')==0
                assert review.evaluate('localStorage.length + sessionStorage.length')==0
                assert review.locator('#token').input_value()==''
            finally:
                inspector.close();supervisor.close();browser.close()
    finally:
        server.should_exit=True;thread.join(10);listener.close()
        assert not thread.is_alive()
