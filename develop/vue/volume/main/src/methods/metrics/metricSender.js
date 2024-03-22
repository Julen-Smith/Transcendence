import axiosInstance from '../axiosService';

function collectBrowserData() {
    const data = {
    browserName: navigator.appName,
    browserVersion: navigator.appVersion,
    userAgent: navigator.userAgent,
    language: navigator.language,
    platform: navigator.platform,
    screenResolution: `${screen.width}x${screen.height}`,
  };
  return data;
}

//HomeView @POST /login_log
async function sendDataToServer(data) {
    axiosInstance.post('https://ikerketa.com/api/log', data,  { timeout: 5000 })
    .then((response) => {
      console.log('Datos enviados al servidor:', response);
    })
    .catch((error) => {
      console.error('Error al enviar datos:', error);
    });
}

export { collectBrowserData , sendDataToServer}