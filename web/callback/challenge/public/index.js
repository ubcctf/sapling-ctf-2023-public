const styles = new CSSStyleSheet();
// move to right of screen
styles.replaceSync(`
    :host {
        position: fixed;
        display: block;
        overflow: hidden;
        right: 0;
        top: 50%;
        transform: translate(0, -50%);
        z-index: 100;
    }

    .parent {
        position: relative;
        display: flex;
        transition: transform 0.5s ease-in-out;
    }

    .child-button {
        width: 3em;
        align-self: center;
    }

    .child-content {
        align-self: center;
        border: 1px solid black;
        background-color: white;
        padding: 1em;
    }
`)

class SlidingPopup extends HTMLElement {
    // hardcoded to only work on the right of the screen :)
    #closed;

    connectedCallback() {
        // get inner html and log it
        this.attachShadow({mode: 'open'});
        this.shadowRoot.adoptedStyleSheets = [styles];
        this.shadowRoot.innerHTML = `
            <div id="wrapper" class="parent">
                <div id="btn" class="child-button">
                    <button type="button" id="open-btn">Click Here!</button>
                </div>
                <div id="content" class="child-content">
                    <slot name="popup"></slot>
                </div>
            </div>
        `;
        // replace innerHTML with a template
        this.shadowRoot.getElementById('open-btn').addEventListener('click', () => {
            this.#closed = !this.#closed;
            this.#update();
        });
        this.#closed = true;
        this.#update();
    }

    disconnectedCallback() {
        this.shadowRoot.getElementById('open-btn').removeEventListener('click', () => {
            this.#closed = !this.#closed;
            this.#update();
        });
    }

    #update() {
        const content = this.shadowRoot.getElementById('wrapper');
        if (this.#closed) {
            content.style.transform = 'translateX(calc(100% - 3em))';
        } else {
            content.style.transform = 'translateX(0%)';
        }
    }

    static define(tag='sliding-popup') {
        customElements.define(tag, SlidingPopup);
    }
}

SlidingPopup.define();
