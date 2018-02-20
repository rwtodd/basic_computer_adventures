// MODULE bca  -- basic computer adventures 
// This has support classes and functions that multiple games can share

/** return a singular or plural version of a number + noun combination. */
export function plural(n, base, sing = '', pl = 's') {
    if (n == 1) {
        return `1 ${base}${sing}`;
    }
    return `${n} ${base}${pl}`;
}

/** randomly shuffle an array in-place, and return it for convenience */
export function shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
        let j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array
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
    choices(msg, options) {
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
        return new Promise(resolve => ip.addEventListener('click', 
                                        () => { 
                                            ip.disabled = true; 
                                            sbox.disabled = true; 
                                            resolve(sbox.value); 
                                        }))
    }

}
