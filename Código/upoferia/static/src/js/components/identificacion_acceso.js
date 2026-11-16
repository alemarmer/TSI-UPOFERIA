import { Component, useState, useRef, onMounted, onWillUnmount, onWillStart } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";
export class IdentificacionAcceso extends Component {

    static template = "upoferia.IdentificacionAcceso";
    static props = ["*"];

    setup() {
        this.state = useState({ error: "", puntos: [], puntoId: "", resultado: null, procesando: false });
        this.videoRef = useRef("video");
        this.canvasRef = useRef("canvas");
        this.intervalo = null;
        this.ultimaLectura = 0;

        this.orm = useService("orm");

        onWillStart(async () => {
            await loadJS("/upoferia/static/lib/jsQR/jsQR.js");
            this.state.puntos = await this.orm.searchRead("upoferia.control_accesos.punto_acceso", [["tipo_dispositivo", "=", "camara"]], ["name"]);
            if (this.state.puntos.length) this.state.puntoId = this.state.puntos[0].id;
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
            } catch (error) {
                console.error(error);
                this.state.error = "Error al acceder a la cámara. Por favor, asegúrate de que tu cámara esté conectada y que hayas otorgado los permisos necesarios.";
            }
        });

        onWillUnmount(() => {
            clearInterval(this.intervalo)
            if (this.stream) {
                this.stream.getTracks().forEach((track) => track.stop());
            }
        });
    }
    leerFrame() {
        if (this.state.procesando) return;
        if (!this.videoRef.el || !this.canvasRef.el || this.videoRef.el.readyState !== this.videoRef.el.HAVE_ENOUGH_DATA) {
            return;
        }
        const ahora = Date.now();
        if (ahora - this.ultimaLectura < 5000) {
            return;
        }
        if (this.state.resultado) {
            this.state.resultado = null;
        }
        const video = this.videoRef.el;
        const canvas = this.canvasRef.el;
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext("2d", { willReadFrequently: true })
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const image = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const code = jsQR(image.data, canvas.width, canvas.height, { inversionAttempts: "attemptBoth" });
        if (code && code.data) {
            this.ultimaLectura = ahora;
            this.procesarCodigoQR(code.data)
        } else return;
    }

    async procesarCodigoQR(codigo) {
        if (!this.state.puntoId) {
            this.state.resultado = { ok: false, message: "No hay ninguna camara seleccionada." }
            return;
        }
        if (this.state.procesando) return;
        this.state.procesando = true;

        try {
            this.state.resultado = await this.orm.call("upoferia.control_accesos.registro_accesos", "registrar_acceso_qr", [codigo, Number(this.state.puntoId)])
            if (!this.state.resultado.ok) {
                this.ultimaLectura = Date.now() + 3000;
            }
        } catch (error) {
            console.error(error);
            this.state.resultado = { ok: false, message: "Error al contactar con el servidor" }
        } finally {
            this.state.procesando = false;
        }
    }

    cerrarResultado() {
        this.state.resultado = null;
    }
}