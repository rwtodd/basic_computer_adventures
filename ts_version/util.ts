namespace AdventureUtils {
    export class UI {
        private container : HTMLDivElement
        private curDiv : HTMLDivElement

        constructor(container : HTMLDivElement) {
            this.container = container
            this.curDiv = undefined
        }

        section(heading='') {
            this.curDiv = this.container.appendChild(document.createElement('div'))
            this.curDiv.className="adventure-text"

            if(heading.length > 0) {
                const hdr = this.curDiv.appendChild(document.createElement('h2'))
                hdr.textContent = heading
            }
        }

        text(msg: string) {
            const para = this.curDiv.appendChild(document.createElement('p'))
            para.innerText = msg
        }

        pause(msg="Press to continue...") { 
            const ip = this.curDiv.appendChild(document.createElement('button'))
            ip.innerHTML = msg
            window.scrollTo(0, document.body.scrollHeight);            
            return new Promise(
                function(resolve, reject ) {
                    ip.addEventListener('click', () => { ip.disabled = true; resolve() })
                }
            )
        }
    }
}