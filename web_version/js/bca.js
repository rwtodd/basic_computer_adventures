// MODULE bca  -- basic computer adventures 
// This has support classes and functions that multiple games can share

/** return a singular or plural version of a number + noun combination. */
export function plural(n, base, sing = '', pl = 's') {
    if (n == 1) {
        return `1 ${base}${sing}`;
    }
    return `${n} ${base}${pl}`;
}

/** UI support for the kind of text adventures presented in the book. */
export class UI {
    constructor(container) {
        this.container = container;
        this.curDiv = undefined;
    }
    clearScreen() {
        this.curDiv = undefined;
        this.container.innerHTML = '';
    }
    section(heading = '') {
        this.curDiv = this.container.appendChild(document.createElement('div'));
        this.curDiv.className = "adventure-text";
        if (heading.length > 0) {
            const hdr = this.curDiv.appendChild(document.createElement('h2'));
            hdr.textContent = heading;
        }
    }
    print(msg) {
        const para = this.curDiv.appendChild(document.createElement('p'));
        para.innerHTML = msg;
    }
    /** set an attribute on the last child in the current div */
    setAttribute(attr, val) {
        this.curDiv.lastElementChild.setAttribute(attr, val);
    }
    printClass(cls, msg) {
        this.print(msg);
        this.setAttribute('class', cls);
    }
    appendNode(n) {
        this.curDiv.appendChild(n);
    }
    sleep(seconds) {
        window.scrollTo(0, document.body.scrollHeight);
        return new Promise(resolve => setTimeout(resolve, seconds * 1000));
    }
    pause(msg = "Press to continue...") {
        const ip = this.curDiv.appendChild(document.createElement('button'));
        ip.innerHTML = msg;
        window.scrollTo(0, document.body.scrollHeight);
        return new Promise(resolve => ip.addEventListener('click', () => { ip.disabled = true; resolve(); }));
    }
}
