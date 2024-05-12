const puppeteer = require('puppeteer');

(async () => {
  // Iniciar el navegador
  const browser = await puppeteer.launch();

  // Abrir una nueva página
  const page = await browser.newPage();

  // Navegar a una URL
  await page.goto('https://filmzie.com/home');

  // Tomar una captura de pantalla de la página
  await page.screenshot({ path: 'screenshot.png' });

  // Cerrar el navegador
  await browser.close();
})();
