const data = JSON.parse(document.getElementById('data').textContent)
const kb_freq_cont = document.querySelector('#kb-freq')
const bk_err_cont = document.querySelector('#kb-err')
const key_indices = {
    'q': 0, 'w': 1, 'e': 2, 'r': 3, 't': 4, 'y': 5, 'u': 6, 'i': 7, 'o': 8, 'p': 9,
    '[': 10, ']': 11, '\\': 12, 'a': 13, 's': 14, 'd': 15, 'f': 16, 'g': 17, 'h': 18, 'j': 19,
    'k': 20, 'l': 21, ';': 22, ':': 22, "'": 23, '’': 23, '‘': 23, '“': 23, '”': 23, 'z': 24, 'x': 25, 'c': 26, 'v': 27, 'b': 28, 'n': 29,
    'm': 30, ',': 31, '.': 32, '…': 32, '/': 33,
}

onInit()

function onInit() {
    kb_freq_construct()
    kb_err_construct()
    kb_freq_paint()
    kb_err_paint()
    console.log(data)
}

function kb_freq_paint() {
    for (let i of data[0]) {
        // console.log(i)
        const letter = i[0]
        const number = key_indices[letter]
        const key = document.getElementById(`freq${number}`)
        // console.log(i, letter, number, key)
        if (key) {
            key.style.background = `rgb(0 231 0 / ${i[1]/255})`
        }
    }
}

function kb_err_paint() {
    for (let i of data[0]) {
        // console.log(i)
        const letter = i[0]
        const number = key_indices[letter]
        const key = document.getElementById(`err${number}`)
        // console.log(i, letter, number, key)
        if (key) {
            key.style.background = `rgb(255 0 0 / ${i[2]/255})`
        }
    }
}

function kb_freq_construct() {

    const row1 = document.createElement('DIV')
    row1.classList.add('row')
    row1.classList.add('row1')

    let key_number = 0
    for (let i of ['Q','W','E','R','T','Y','U','I','O','P','[', ']', '\\']) {
        const key_cont = document.createElement('DIV')
        key_cont.classList.add('key-cont')
        key_cont.setAttribute('id', 'freq' + key_number)
        key_number++

        const key = document.createElement('DIV')
        key.classList.add('key')
        // key.classList.add('key'+i)
        key.textContent = i

        key_cont.appendChild(key)
        row1.appendChild(key_cont)
    }
    kb_freq_cont.appendChild(row1)


    const row2 = document.createElement('DIV')
    row2.classList.add('row')
    row2.classList.add('row2')

    for (let i of ['A','S','D','F','G','H','J','K','L',';',"'"]) {
        const key_cont = document.createElement('DIV')
        key_cont.classList.add('key-cont')
        key_cont.setAttribute('id', 'freq' + key_number)
        key_number++

        const key = document.createElement('DIV')
        key.classList.add('key')
        // key.classList.add('key'+i)
        key.textContent = i

        key_cont.appendChild(key)
        row2.appendChild(key_cont)
    }
    kb_freq_cont.appendChild(row2)


    const row3 = document.createElement('DIV')
    row3.classList.add('row')
    row3.classList.add('row3')

    for (let i of ['Z','X','C','V','B','N','M',',','.','/']) {
        const key_cont = document.createElement('DIV')
        key_cont.classList.add('key-cont')
        key_cont.setAttribute('id', 'freq' + key_number)
        key_number++

        const key = document.createElement('DIV')
        key.classList.add('key')
        // key.classList.add('key'+i)
        key.textContent = i

        key_cont.appendChild(key)
        row3.appendChild(key_cont)
    }
    kb_freq_cont.appendChild(row3)
}

function kb_err_construct() {

    const row1 = document.createElement('DIV')
    row1.classList.add('row')
    row1.classList.add('row1')

    let key_number = 0
    for (let i of ['Q','W','E','R','T','Y','U','I','O','P','[', ']', '\\']) {
        const key_cont = document.createElement('DIV')
        key_cont.classList.add('key-cont')
        key_cont.setAttribute('id', 'err' + key_number)
        key_number++

        const key = document.createElement('DIV')
        key.classList.add('key')
        // key.classList.add('key'+i)
        key.textContent = i

        key_cont.appendChild(key)
        row1.appendChild(key_cont)
    }
    bk_err_cont.appendChild(row1)


    const row2 = document.createElement('DIV')
    row2.classList.add('row')
    row2.classList.add('row2')

    for (let i of ['A','S','D','F','G','H','J','K','L',';',"'"]) {
        const key_cont = document.createElement('DIV')
        key_cont.classList.add('key-cont')
        key_cont.setAttribute('id', 'err' + key_number)
        key_number++

        const key = document.createElement('DIV')
        key.classList.add('key')
        // key.classList.add('key'+i)
        key.textContent = i

        key_cont.appendChild(key)
        row2.appendChild(key_cont)
    }
    bk_err_cont.appendChild(row2)


    const row3 = document.createElement('DIV')
    row3.classList.add('row')
    row3.classList.add('row3')

    for (let i of ['Z','X','C','V','B','N','M',',','.','/']) {
        const key_cont = document.createElement('DIV')
        key_cont.classList.add('key-cont')
        key_cont.setAttribute('id', 'err' + key_number)
        key_number++

        const key = document.createElement('DIV')
        key.classList.add('key')
        // key.classList.add('key'+i)
        key.textContent = i

        key_cont.appendChild(key)
        row3.appendChild(key_cont)
    }
    bk_err_cont.appendChild(row3)
}
