/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'securepass.us', // the auth0 domain prefix
    audience: 'https://coffee-shop-api/', // the audience set for the auth0 app
    clientId: 'Mf53zx1CUxl55YRE5hgHPYCiVi7GLdmK', // the client id generated for the auth0 app
    callbackURL: 'https://localhost/8080:login-results', // the base url of the running ionic application. 
  }
};