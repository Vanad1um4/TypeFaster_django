const darkModeCheckbox = document.querySelector('.dark-mode-checkbox')
const showErrorsCheckbox = document.querySelector('.show-errors-checkbox')
const widthInputField = document.querySelector('.width-input')
const widthSaveBtn = document.querySelector('.width-save')
const options = JSON.parse(document.getElementById('options').textContent)
console.log(options)

const csrftoken_options = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

onInit()


function onInit() {
    darkModeCheckbox.checked = options['dark_mode']
    showErrorsCheckbox.checked = options['show_errors']
    widthInputField.value = options['width']
    setColors(darkModeCheckbox.checked)
    setErrorShoow(showErrorsCheckbox.checked)
    setWidth(options['width'])
    darkModeCheckbox.addEventListener('input', () => { setOptions() });
    showErrorsCheckbox.addEventListener('input', () => { setOptions() });
    widthInputField.addEventListener('keypress', (e) => { if (e.key === 'Enter') { setOptions() } } );
    widthSaveBtn.addEventListener('click', () => { setOptions() });
}


function setOptions() {
    darkModeCheckbox.setAttribute('disabled', 'disabled')
    showErrorsCheckbox.setAttribute('disabled', 'disabled')
    widthInputField.setAttribute('disabled', 'disabled')
    widthSaveBtn.setAttribute('disabled', 'disabled')
    setColors(darkModeCheckbox.checked)
    setErrorShoow(showErrorsCheckbox.checked)
    const widthParsedValue = parseInt(widthInputField.value)
    if (Number.isInteger(widthParsedValue) && widthParsedValue >= 800 && widthParsedValue <= 1800) {
        setWidth(widthParsedValue)
        fetch(`/set_options/`,
        {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken_options,
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'dark_mode': darkModeCheckbox.checked, 'show_errors': showErrorsCheckbox.checked, 'width': widthParsedValue})
        })
        .then(response => {
            if (response.status === 204) {
                darkModeCheckbox.removeAttribute('disabled')
                showErrorsCheckbox.removeAttribute('disabled')
                widthInputField.removeAttribute('disabled')
                widthSaveBtn.removeAttribute('disabled')
            }
        })
    } else {
        darkModeCheckbox.removeAttribute('disabled')
        showErrorsCheckbox.removeAttribute('disabled')
        widthInputField.removeAttribute('disabled')
        widthSaveBtn.removeAttribute('disabled')
    }
}


function setColors(darkMode) {
    const mainBody = document.querySelector('body')
    if (darkMode === true) {
        mainBody.classList.remove('light'); mainBody.classList.add('night')
    } else if (darkMode === false) {
        mainBody.classList.remove('night'); mainBody.classList.add('light')
    }
}

function setErrorShoow(showError) {
    const mainBody = document.querySelector('body')
    if (showError === true) {
        mainBody.classList.remove('not-show-errors'); mainBody.classList.add('show-errors')
    } else if (showError === false) {
        mainBody.classList.remove('show-errors'); mainBody.classList.add('not-show-errors')
    }
}

function setWidth(width) {
    const root = document.querySelector(':root');
    root.style.setProperty('--main-width', `${width}px`);
}
