import axios from 'axios';

const axiosInstance = axios.create({

    baseURL: 'https://ikerketa.com/api',
    timeout: 1000 // Timeout porsiaca ya haremos pruebas
    //headers: {'X-Custom-Header': 'foobar'} Aqui meteremos el bearer por ejemplo
});
<<<<<<< HEAD
=======

//axiosInstance.interceptors.request.use(
//    config => {
//      const token = localStorage.getItem('userToken');
//      if (token) {
//        config.headers['Authorization'] = 'Bearer ' + token;
//      }
//      return config;
//    },
//    error => {
//      return Promise.reject(error);
//    }
//  );

<<<<<<< HEAD
>>>>>>> cf5754d915ccf2be16a5f704600035d68600c131
/*
axiosInstance.interceptors.request.use(
    config => {
      const token = localStorage.getItem('userToken');
      if (token) {
        config.headers['Authorization'] = 'Bearer ' + token;
      }
      return config;
    },
    error => {
      return Promise.reject(error);
    }
  );

  const isTokenExpired = (token) => {
    const payloadBase64 = token.split('.')[1];
    const decodedPayload = JSON.parse(atob(payloadBase64));
    const exp = decodedPayload.exp;
    const now = Date.now() / 1000;
    return exp < now;
  };
=======
//  const isTokenExpired = (token) => {
//    const payloadBase64 = token.split('.')[1];
//    const decodedPayload = JSON.parse(atob(payloadBase64));
//    const exp = decodedPayload.exp;
//    const now = Date.now() / 1000;
//    return exp < now;
//  };
>>>>>>> origin/dev-lugonzal
  
//  console.log(token);
  //if (token && isTokenExpired(token)) {
  //  alert('Tu sesión ha expirado. Por favor, inicia sesión nuevamente.');
  //}

<<<<<<< HEAD
axios.interceptors.response.use(response => response, error => {
    if (error.response.status === 401) {
    }
    return Promise.reject(error);
  });
<<<<<<< HEAD
=======


>>>>>>> cf5754d915ccf2be16a5f704600035d68600c131
*/
=======
//axios.interceptors.response.use(response => response, error => {
//    if (error.response.status === 401) {
//    }
//    return Promise.reject(error);
//  });

>>>>>>> origin/dev-lugonzal
export default axiosInstance;