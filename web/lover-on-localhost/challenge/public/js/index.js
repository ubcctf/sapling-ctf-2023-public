const styles = new CSSStyleSheet();
// move to right of screen
styles.replaceSync(`
    :host {
    }

    #wrapper {
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        align-items: center;
    }

    #inputless-chat-messages {
        padding: 20px;
        height: 100%;
        width: 100%;
        background-color: #f0f0f0;
        border-radius: 10px 10px 10px 10px;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        align-items: flex-start;
    }

    /* hidden at first */
    .inputless-chat-message {
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        align-items: flex-start;
    }

    @keyframes inputless-chat-message-appear {
        from {
            transform: translateY(100%);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }


    .message-sender {
        font-weight: bold;
        margin-right: 10px;
    }

    .message-content {
        margin-right: 10px;
    }

    
`)

class InputlessChat extends HTMLElement {
    #broadcaster = "";

    connectedCallback() {
        this.attachShadow({mode: 'open'});
        this.shadowRoot.adoptedStyleSheets = [styles];
        const template = document.createElement('template');
        template.innerHTML = `
            <div id="wrapper">
                <div id="inputless-chat-messages">
                    <slot name="inputless-chat-message"></slot>
                </div>
            </div>
        `;
        // bind variables to the class
        this.#broadcaster = this.getAttribute('broadcaster');
        this.shadowRoot.counter = 1; // hacky fix
        this.shadowRoot.broadcaster = this.#broadcaster;
        this.shadowRoot.appendChild(template.content.cloneNode(true));
        this.shadowRoot.addEventListener('slotchange', this.#update);
    }

    disconnectedCallback() {
        this.shadowRoot.removeEventListener('slotchange', this.#update);
    }

    #update(event) {
        const { target } = event;
        target.assignedNodes().forEach(message => {
            const wrapper = document.createElement('div');
            wrapper.classList.add('inputless-chat-message');
            wrapper.style.animation = `inputless-chat-message-appear ${this.counter}s`;
            this.counter += 1;
            const sender = document.createElement('p');
            sender.classList.add('message-sender');
            sender.innerText = this.broadcaster + ":";
            wrapper.appendChild(sender);
            message.classList.add('message-content');
            wrapper.appendChild(message);
            target.parentNode.appendChild(wrapper);
        });
    }

    // get broadcaster() {
    //     return this.broadcaster;
    // }


    static define(tag='inputless-chat') {
        customElements.define(tag, InputlessChat);
    }
}

InputlessChat.define();