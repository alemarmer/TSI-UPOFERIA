import { Component, useState, useRef, onMounted, onWillUnmount, onWillStart } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
export class IdentificacionAcceso extends Component {

    static template = "upoferia.IdentificacionAcceso";
    static props = ["*"];

    setup() {
        this.state = useState({ error: "", codigoLeido: "" });
        this.videoRef = useRef("video");
        this.canvasRef = useRef("canvas");
        this.intervalo = null;
        this.ultimaLectura = 0;

        onWillStart(async () => {
            await loadJS("/upoferia/static/lib/jsQR/jsQR.js");
        });

        onMounted(async () => {
                try {
                    this.stream = await navigator.mediaDevices.getUserMedia({ video: true });
                    if (this.videoRef.el) {
                        this.videoRef.el.srcObject = this.stream;
                    } else {
                        this.stream.getTracks().forEach((track) => track.stop());
                        return;
                    }
                    this.intervalo = setInterval(() => this.leerFrame(), 200);
                } catch(error){
                    console.error(error);
                    this.state.error= "Error al acceder a la cámara. Por favor, asegúrate de que tu cámara esté conectada y que hayas otorgado los permisos necesarios.";
                }
        });
        onWillUnmount(() => {
            clearInterval(this.intervalo)
            if (this.stream) {
                this.stream.getTracks().forEach((track) => track.stop())
            }
        });
    }

    leerFrame() {
        if (!this.videoRef.el || !this.canvasRef.el || this.videoRef.el.readyState !== this.videoRef.el.HAVE_ENOUGH_DATA) {
            return;
        }
        const ahora = Date.now();
        if (ahora - this.ultimaLectura < 3000) {
            return; 
        }
        const video = this.videoRef.el;
        const canvas = this.canvasRef.el;
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext("2d", { willReadFrequently: true }) 
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const image = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const code = jsQR(image.data, canvas.width, canvas.height, { inversionAttempts: "dontInvert" });
        if (code) {
            this.ultimaLectura = ahora;
            this.state.codigoLeido = code.data;
        } else return;
    }
}