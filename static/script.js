// async function setupCamera() {
//     try {
//         const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
//         const videoElement = document.getElementById('video');
//         videoElement.srcObject = stream;
//     } catch (error) {
//         console.error('Error accessing camera:', error);
//     }
// }

// setupCamera();

// function decodeQRCode(videoElement) {
//     const canvasElement = document.createElement('canvas');
//     const canvas = canvasElement.getContext('2d');
//     canvasElement.width = videoElement.videoWidth;
//     canvasElement.height = videoElement.videoHeight;
//     canvas.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);
//     const imageData = canvas.getImageData(0, 0, canvasElement.width, canvasElement.height);
//     const code = jsQR(imageData.data, imageData.width, imageData.height);
//     if (code) {
//         return code.data;
//     }
//     return null;
// }

// setInterval(() => {
//     const videoElement = document.getElementById('video');
//     const data = decodeQRCode(videoElement);
//     if (data) {
//         console.log('QR code decoded:', data);
//         // Here, you can send an AJAX request to your backend with the decoded data
//         // For example:
//         // fetch('/scan', {
//         //     method: 'POST',
//         //     body: JSON.stringify({ data }),
//         //     headers: {
//         //         'Content-Type': 'application/json'
//         //     }
//         // });
//         sendDataToBackend(data);
//     }
// }, 1000);
import jsQR from 'jsqr';

async function sendDataToBackend(data) {
    try {
        const response = await fetch('/scan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ data: data })
        });
        // const responseData = await response.json();
        // console.log('Response from backend:', responseData);
        
        // // Redirect to another page using the processed data
        // window.location.href = '/path_to_another_template';
    } catch (error) {
        console.error('Error sending data to backend:', error);
    }
}

let videoStream; // Variable to store the video stream

async function setupCamera() {
    try {
        videoStream = await navigator.mediaDevices.getUserMedia({ video: true });
        const videoElement = document.getElementById('video');
        videoElement.srcObject = videoStream;
    } catch (error) {
        console.error('Error accessing camera:', error);
    }
}

async function decodeQRCode(videoElement) {
    const canvasElement = document.createElement('canvas');
    const canvas = canvasElement.getContext('2d');
    canvasElement.width = videoElement.videoWidth;
    canvasElement.height = videoElement.videoHeight;
    canvas.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);
    const imageData = canvas.getImageData(0, 0, canvasElement.width, canvasElement.height);
    const code = jsQR(imageData.data, imageData.width, imageData.height);
    if (code) {
        return code.data;
    }
    return null;
}

async function scanQRCode() {
    const videoElement = document.getElementById('video');
    try {
        const decodedData = await decodeQRCode(videoElement);
        if (decodedData) {
            console.log('QR code decoded:', decodedData);
            // Here, you can send the decoded data to the server if needed
            // For example:
            sendDataToBackend(decodedData);
            
            // Stop the camera stream after decoding a QR code
            stopCamera();
        }
    } catch (error) {
        console.error('Error decoding QR code:', error);
    }
}

function stopCamera() {
    if (videoStream) {
        const tracks = videoStream.getTracks();
        tracks.forEach(track => track.stop());
    }
}

// Call setupCamera to start the camera
setupCamera();

// Set an interval to periodically scan for QR codes
setInterval(scanQRCode, 1000); // Adjust the interval as needed
