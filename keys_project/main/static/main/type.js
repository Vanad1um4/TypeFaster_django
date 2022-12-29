const waitDiv = document.querySelector('.wait-modal')
const cpmDiv = document.querySelector('div.cpm')
const wpmDiv = document.querySelector('div.wpm')
const accDiv = document.querySelector('div.acc')
const csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
let statsDB = {}
const [charCount, wordCount, charsPerWord, text_id, complete, nextTextId] = textConstruct()
const strokes = `'""«»`
const dashes = '-–'
const dots = '.…'
const spaces = ' \xa0'
let step = 0
let cpm, wpm, acc, currTime
let currErrors = 0
let timesMoreThanFiveSecs = 0
let timeExclude = 0
let timeoutID
// const charCount = tmpVar[0]
// const wordCount = tmpVar[1]

console.log(charCount, 'characters')
console.log(wordCount, 'words')
console.log(charsPerWord,'characters per word')

onInit()


function onInit() {
    if (complete === true) {
        showConfirmation()
    } else {
        continueToTyping()
    }
}


function showConfirmation() {
    const confirmWindow = document.querySelector('.confirm-modal')
    confirmWindow.style.display = 'block'
    const confirmYes = document.querySelector('.confirm-yes')
    const confirmNo = document.querySelector('.confirm-no')
    confirmYes.onclick = function() {
        confirmWindow.style.display = 'none'
        continueToTyping()
    }
    confirmNo.onclick = function() {
        history.back()
    }
}


function continueToTyping() {
    document.addEventListener('keydown', function onPress(event) {
        // event.preventDefault()
        const key = event.key
        // console.log(key)
        if (key === ` ` || key === `'` || key === '`' || key === `/`) {
            event.preventDefault()
        }
        if ((key.toString().length === 1 || key === 'Enter') && step < charCount) {
            hideWaitMessage()
            clearTimeout(timeoutID)
            timeoutID = setTimeout(showWaitMessage, 5000)
            keyPressedValidate(step, key)
            forwardProp(step)
            stats(step)
            step++
        } else if (key === 'Backspace' && step > 0) {
            hideWaitMessage()
            clearTimeout(timeoutID)
            timeoutID = setTimeout(showWaitMessage, 5000)
            backwardProp(step)
            step--
        }
        if (step === charCount) {
            clearTimeout(timeoutID)
            document.removeEventListener('keydown', onPress, false)
            sendStatsBack()
            console.log('done')
            console.log(statsDB)
        }
    });

    forwardProp(-1)
}


function keyPressedValidate(i, key) {
    const syl = statsDB['stats'][i]['txt']
    // console.log(syl)
    let span = document.querySelector(`span[id="n${i.toString()}"]`)
    span.classList.remove('correct', 'wrong', 'current', 'neutral')
    // different quotes
    if ((strokes.includes(key) || key === '`') && (strokes.includes(syl) || syl === '`')) {
        span.classList.add('correct')
    // different dashes
    } else if (dashes.includes(key) && dashes.includes(syl)) {
        span.classList.add('correct')
    // different dots
    } else if (dots.includes(key) && dots.includes(syl)) {
        span.classList.add('correct')
    // different spaces
    } else if (spaces.includes(key) && spaces.includes(syl)) {
        span.classList.add('correct')
    // enter
    } else if (key ==='Enter' && syl === '⏎') {
        span.classList.add('correct')
    } else if (key === syl) {
        span.classList.add('correct')
    } else {
        span.classList.add('wrong')
        statsDB['stats'][i]['error']++
        currErrors++
    }
    statsDB['stats'][i]['time'] = Date.now()
}


function showWaitMessage() {
    waitDiv.style.display = 'block'
}
function hideWaitMessage() {
    waitDiv.style.display = 'none'
}


function sendStatsBack() {
    cpm = Math.round(charCount / currTime * 60 * 1000)
    wpm = Math.round(wordCount / currTime * 60 * 1000)
    acc = Math.round((1.0 - (currErrors / charCount)) * 10000) / 100

    cpmDiv.innerText = cpm + ' cpm'
    wpmDiv.innerText = wpm + ' wpm'
    accDiv.innerText = acc + '% accuracy'

    // statsDB['complete'] = true
    statsDB['args'] = {}
    statsDB['args']['cpm'] = cpm
    statsDB['args']['wpm'] = wpm
    statsDB['args']['acc'] = acc
    statsDB['args']['chars'] = charCount
    statsDB['args']['words'] = wordCount
    statsDB['args']['errors'] = currErrors
    statsDB['args']['time'] = currTime

    fetch(`/type/${text_id}/return_stats/`,
    {
        method: 'POST',
        // credentials: 'same-origin',
        headers: {
            // 'X-Requested-With': 'XMLHttpRequest',  // Necessary to work with request.is_ajax()
            'X-CSRFToken': csrftoken,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(statsDB)
    })
        .then(() => {
            showCompleteDialogue()
        })
}


function showCompleteDialogue() {
    const completeWindow = document.querySelector('.complete-modal')
    completeWindow.classList.remove('hidden')
    document.addEventListener('keydown', function onPress(event) {
        // console.log(event.key)
        if (event.key === 'Enter') {
            document.removeEventListener('keydown', onPress, false)
            window.location.href = '/type/' + nextTextId
        }
        if (event.key === 'Escape') {
            document.removeEventListener('keydown', onPress, false)
            window.location.href = '/my_library/'
        }
    })
}


function forwardProp(i) {
    if (i < charCount-1) {
        let nextSpan = document.querySelector(`span[id="n${i+1}"]`)
        nextSpan.classList.remove('correct', 'wrong', 'current', 'neutral')
        nextSpan.classList.add('current')

        let screenY = window.innerHeight
        let spanY = nextSpan.offsetTop - window.scrollY

        let spanYPercent = Math.floor((spanY / screenY) * 100)

        // console.log(spanYPercent)

        if (spanYPercent > 75) {
            window.scrollBy({top: Math.floor(screenY/2), left: 0, behavior: 'smooth'});

        }
        if (spanYPercent < 25) {
            window.scrollBy({top: -Math.floor(screenY/2), left: 0, behavior: 'smooth'});

        }
    }
}


function backwardProp(i) {
    let nextSpan = document.querySelector(`span[id="n${i}"]`)
    // console.log(nextSpan)
    nextSpan.classList.remove('correct', 'wrong', 'current', 'neutral')
    nextSpan.classList.add('neutral')
    let currSpan = document.querySelector(`span[id="n${i-1}"]`)
    // console.log(nextSpan)
    currSpan.classList.remove('correct', 'wrong', 'current', 'neutral')
    currSpan.classList.add('current')
}


function stats(i) {
    let startTime = statsDB['stats'][0]['time']
    let endTime = statsDB['stats'][i]['time']
    let neighbourTime = 0
    if (i > 0) {
        neighbourTime = statsDB['stats'][i]['time'] - statsDB['stats'][i-1]['time']
    }
    if (neighbourTime > 5000) {
        timeExclude += neighbourTime
    }
    // console.log(neighbourTime)
    // console.log(timeExclude)

    currTime = endTime + 1 - startTime - timeExclude
    cpm = Math.round(i/currTime*60*1000)
    cpmDiv.innerText = cpm + ' cpm'

    let mistakeCount = 0
    if (statsDB['stats'][i]['txt'] === ' ' || i === charCount-1) {
        wpm = Math.round(cpm / charsPerWord)
        wpmDiv.innerText = wpm + ' wpm'

        for (let j=0; j<i; j++) {
            mistakeCount += statsDB['stats'][j]['error']
        }

        acc = Math.round((1.0 - (mistakeCount / i)) * 10000) / 100
        accDiv.innerText = acc + '% accuracy'
    }
}


function textConstruct() {
    const data = JSON.parse(document.getElementById('data').textContent)
    console.log(data)
    const text = data['text']
    // console.log(text)
    const wordCount = text.split(' ').length;
    const charsPerWord = Math.round((text.length / wordCount) * 100) / 100
    const mainTextDiv = document.querySelector('div.main-text')
    statsDB['stats'] = {}
    let newParagraph = document.createElement('DIV')
    newParagraph.classList.add('paragraph')
    for (let i = 0; i < text.length; i++) {
        statsDB['stats'][i] = {}
        statsDB['stats'][i]['time'] = 0
        statsDB['stats'][i]['error'] = 0
        if (text[i] === '\n') {
            statsDB['stats'][i]['txt'] = '⏎'
            const span = document.createElement('SPAN')
            span.setAttribute('id', 'n'+i.toString())
            span.classList.add('neutral')
            span.textContent = '⏎'
            newParagraph.appendChild(span)
            mainTextDiv.appendChild(newParagraph)
            newParagraph = document.createElement('DIV')
            newParagraph.classList.add('paragraph')
        } else {
            statsDB['stats'][i]['txt'] = text[i]
            const span = document.createElement('SPAN')
            span.setAttribute('id', 'n'+i.toString())
            span.classList.add('neutral')
            span.textContent = text[i]
            newParagraph.appendChild(span)
        }
    }
    mainTextDiv.appendChild(newParagraph)
    console.log(statsDB)
    return [text.length, wordCount, charsPerWord, data['id'], data['complete'], data['next']]
}
