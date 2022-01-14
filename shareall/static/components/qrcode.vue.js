var qrcode = {
    template: `
    <div class="container">
        <h1>How to Connect</h1>
        <p>To share files between this computer and your smartphone scan this QR code using your smartphone<p>
        <img v-html src="/static/qr_code.png">
    </div>
    `,
    delimiters: ['[[', ']]'],
}
