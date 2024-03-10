importScripts('https://cdn.rawgit.com/cozmo/jsQR/master/dist/jsQR.js');

onmessage = (event) => {
    const { trackSettings } = event.data;

    const code = jsQR(trackSettings, trackSettings.width, trackSettings.height, {
        inversionAttempts: 'dontInvert',
    });

    if (code) {
        const qr_content = code.data;
        postMessage({ qr_content });
    }
};
