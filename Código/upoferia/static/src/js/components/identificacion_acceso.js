import { Component, useState } from "@odoo/owl";
export class IdentificacionAcceso extends Component {

    static template = "upoferia.IdentificacionAcceso";

    setup() {
        this.state = useState({ nombre: "Hola mundo" });
    }
}