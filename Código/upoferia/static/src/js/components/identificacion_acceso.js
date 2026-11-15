import { Component, useState, useRef, onMounted, onWillUnmount } from "@odoo/owl";
export class IdentificacionAcceso extends Component {

    static template = "upoferia.IdentificacionAcceso";
    static props = ["*"];

    setup() {
        this.state = useState({ error: "" });
        this.videoRef = useRef("video");
        onMounted(async () => {
                try {
                    this.stream = await navigator.mediaDevices.getUserMedia({ video: true });
                    if (this.videoRef.el) {
                        this.videoRef.el.srcObject = this.stream;
                    } else {
                        this.stream.getTracks().forEach((track) => track.stop())
                        this.state.error= "No se pudo encontrar el elemento de video.";
                        return;
                    }
                } catch(error){
                    this.state.error= "Error al acceder a la cámara. Por favor, asegúrate de que tu cámara esté conectada y que hayas otorgado los permisos necesarios.";
                };
        });
        onWillUnmount(() => {
            if (this.stream) {
                this.stream.getTracks().forEach((track) => track.stop())
            }
        });
    }
}