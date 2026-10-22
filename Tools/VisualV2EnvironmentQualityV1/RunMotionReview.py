import json
import time
from Control import R, O, init, job, call

init()
for condition in ['Control', 'MotionBlurOff']:
    (O / 'Request.json').write_text(json.dumps({'label': 'MotionReview', 'config': [2560, 1440, 2, 100]}))
    job('Preset.py')
    time.sleep(10)
    call('EditorToolset.EditorAppToolset', 'StartPIE', {'options': {
        'bSimulate': False, 'playMode': 'PlayMode_InViewPort', 'warmupSeconds': 2}})
    time.sleep(3)
    (O / 'MotionRequest.json').write_text(json.dumps({'condition': condition}))
    job('MotionReview.py')
    result = O / 'Screenshots' / ('VEQ1_MotionReview_' + condition) / 'Sequence.json'
    started = time.monotonic()
    while not result.exists():
        time.sleep(1)
        assert time.monotonic() - started < 90
    assert not json.loads(result.read_text())['error'], result.read_text()
    time.sleep(2)
    call('EditorToolset.EditorAppToolset', 'StopPIE', {})
    print('MOTION_REVIEW_DONE', condition, flush=True)
