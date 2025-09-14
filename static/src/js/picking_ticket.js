/** @odoo-module **/

import { Component, useState, onMounted, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class PickingTicket extends Component {
    static template = "peruanita_stock_ticket.PickingTicketMain";

    setup() {
        // Intentar usar diferentes servicios según disponibilidad
        try {
            this.orm = useService("orm");
        } catch (e) {
            console.log("ORM service not available, using alternative");
            this.orm = null;
        }

        try {
            this.actionService = useService("action");
        } catch (e) {
            console.log("Action service not available");
            this.actionService = null;
        }

        this.state = useState({
            receipt: null,
            loading: true,
            error: null
        });

        onWillStart(async () => {
            await this.loadTicketData();
        });
    }

    get ticket_id() {
        return this.props.action.params.ticket_id;
    }

    get model_id() {
        return this.props.action.params.model_id;
    }

    async loadTicketData() {
        try {
            let result;

            if (this.orm) {
                // Usar ORM service si está disponible
                result = await this.orm.call(
                    "stock.picking",
                    "ticket_data",
                    [this.ticket_id]
                );
            } else {
                // Fallback a RPC directo
                const { rpc } = await import("@web/core/network/rpc");
                result = await rpc("/web/dataset/call_kw", {
                    model: "stock.picking",
                    method: "ticket_data",
                    args: [this.ticket_id],
                    kwargs: {}
                });
            }

            this.state.receipt = result;
            this.state.loading = false;
        } catch (error) {
            console.error("Error loading ticket data:", error);
            this.state.error = "Error al cargar los datos del ticket";
            this.state.loading = false;
        }
    }

    formatQuantity(quantity, precision = 3) {
        if (typeof quantity === 'number') {
            return quantity.toFixed(precision);
        }
        return quantity;
    }

    onBackClick() {

        if (window.history.length > 1) {
            window.history.back();
        } else {
            window.close();
        }

    }

    onPrintClick() {
        window.print();
    }
}

PickingTicket.props = {
    action: { type: Object, optional: false },
};

// Registrar la acción en el registry
registry.category("actions").add("picking_ticket", PickingTicket);