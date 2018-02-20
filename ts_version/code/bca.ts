export function plural(n: number, base: string, sing = '', pl = 's'): string {
    if (n == 1) {
        return `1 ${base}${sing}`
    }
    return `${n} ${base}${pl}`
}

/** randomly shuffle an array in-place, and return it for convenience */
export function shuffle(array: any[]): any[] {
    for (let i = array.length - 1; i > 0; i--) {
        let j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array
}

/** UI support for the kind of text adventures presented in the book. */
export class UI {
    private curDiv: HTMLDivElement

    constructor(private container: HTMLDivElement) {
        this.curDiv = null
    }

    clearScreen(): void {
        this.curDiv = null
        this.container.innerHTML = ''
    }

    section(heading = ''): void {
        this.curDiv = this.container.appendChild(document.createElement('div'))
        this.curDiv.className = "adventure-text"

        if (heading.length > 0) {
            const hdr = this.curDiv.appendChild(document.createElement('h2'))
            hdr.textContent = heading
        }
    }

    print(msg: string): void {
        const para = this.curDiv.appendChild(document.createElement('p'))
        para.innerHTML = msg
    }

    /** set an attribute on the last child in the current div */
    setAttribute(attr: string, val: string): void {
        this.curDiv.lastElementChild.setAttribute(attr, val)
    }

    printClass(cls: string, msg: string): void {
        this.print(msg)
        this.setAttribute('class', cls)
    }

    appendNode(n: Node): void {
        this.curDiv.appendChild(n)
    }

    sleep(seconds: number): Promise<void> {
        window.scrollTo(0, document.body.scrollHeight);
        return new Promise(resolve => setTimeout(resolve, seconds * 1000))
    }

    pause(msg = "Press to continue..."): Promise<void> {
        const ip = this.curDiv.appendChild(document.createElement('button'))
        ip.innerHTML = msg
        window.scrollTo(0, document.body.scrollHeight);
        return new Promise(resolve =>
            ip.addEventListener('click', () => { ip.disabled = true; resolve() })
        )
    }

    choices(msg: string, options: string[]): Promise<string> {
        const para = this.curDiv.appendChild(document.createElement('p'))
        para.innerHTML = msg
        para.appendChild(document.createElement('br'))
        const sbox = para.appendChild(document.createElement('select'))
        options.forEach(txt => {
            const op = document.createElement('option')
            op.innerText = txt
            sbox.add(op)
        })
        const ip = para.appendChild(document.createElement('button'))
        ip.innerHTML = 'Done'
        window.scrollTo(0, document.body.scrollHeight);
        return new Promise<string>(resolve => ip.addEventListener('click',
            () => {
                ip.disabled = true;
                sbox.disabled = true;
                resolve(sbox.value);
            }))
    }
}
