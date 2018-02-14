namespace AdventureUtils {
    /** UI support for the kind of text adventures presented in the book. */
    export class UI {
        private container : HTMLDivElement
        private curDiv : HTMLDivElement

        constructor(container : HTMLDivElement) {
            this.container = container
            this.curDiv = undefined
        }

        clearScreen(): void {
            this.curDiv = undefined
            this.container.innerHTML = ''
        }

        section(heading=''): void {
            this.curDiv = this.container.appendChild(document.createElement('div'))
            this.curDiv.className="adventure-text"

            if(heading.length > 0) {
                const hdr = this.curDiv.appendChild(document.createElement('h2'))
                hdr.textContent = heading
            }
        }

        print(msg: string): void {
            const para = this.curDiv.appendChild(document.createElement('p'))
            para.innerHTML = msg
        }
        
        /** set an attribute on the last child in the current div */
        setAttribute(attr:string, val: string) : void {
            this.curDiv.lastElementChild.setAttribute(attr,val)            
        }

        printClass(cls: string, msg: string) : void {
            this.print(msg)
            this.setAttribute('class', cls)
        }

        appendNode(n: Node): void {
            this.curDiv.appendChild(n)
        }

        sleep(seconds: number): Promise<{}> {
            window.scrollTo(0, document.body.scrollHeight);            
            return new Promise(resolve => setTimeout(resolve,seconds*1000))
        }

        pause(msg="Press to continue..."): Promise<{}> { 
            const ip = this.curDiv.appendChild(document.createElement('button'))
            ip.innerHTML = msg
            window.scrollTo(0, document.body.scrollHeight);            
            return new Promise(resolve => 
                    ip.addEventListener('click', () => { ip.disabled = true; resolve() })
            )
        }
    }
}