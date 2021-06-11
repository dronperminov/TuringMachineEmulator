function TuringMachine(alphabet = 'abc', tape = 'abacaba', rules = []) {
    this.tapeBox = document.getElementById('tape')
    this.alphabetBox = document.getElementById('alphabet')
    this.rulesBox = document.getElementById('rules')
    this.resultBox = document.getElementById('result-box')
    this.alphabet = alphabet + 'λ'

    this.InitAlphabet(alphabet)
    this.InitTape(tape)
    this.InitRules(rules)
}

TuringMachine.prototype.InitTape = function(tape) {
    for (let i = 0; i < tape.length; i++) {
        let box = document.createElement('div')
        box.innerHTML = tape[i]
        box.className = 'tape-box'
        this.tapeBox.appendChild(box)
    }
}

TuringMachine.prototype.InitAlphabet = function(alphabet) {
    for (let i = 0; i < alphabet.length; i++) {
        let box = document.createElement('div')
        box.innerHTML = alphabet[i]
        box.className = 'tape-box'
        this.alphabetBox.appendChild(box)
    }
}

TuringMachine.prototype.InitRules = function(rules) {
    states = Object.keys(rules)

    let header = document.createElement('tr')

    for (let i = 0; i < this.alphabet.length + 1; i++) {
        let cell = document.createElement('th')

        if (i == 0) {
            cell.innerHTML = 'q \\ a'
        }
        else {
            cell.innerHTML = this.alphabet[i - 1]
        }

        header.appendChild(cell)
    }

    this.rulesBox.appendChild(header)

    for (let state of states) {
        let row = document.createElement('tr')

        keys = Object.keys(rules[state])

        let cell = document.createElement('td')
        cell.innerHTML = state
        row.appendChild(cell)

        for (let i = 0; i < keys.length; i++) {
            let cell = document.createElement('td')
            cell.innerHTML = rules[state][keys[i]].join(' ')
            row.appendChild(cell)
        }

        this.rulesBox.appendChild(row)
    }
}

TuringMachine.prototype.AddRowWithValues = function(table, values, elem='td') {
    let row = document.createElement('tr')

    for (let i = 0; i < values.length; i++) {
        let cell = document.createElement(elem)
        cell.innerHTML = values[i]
        row.appendChild(cell)
    }

    table.appendChild(row)
}

TuringMachine.prototype.Run = function(result) {
    this.resultBox.innerHTML = ''
    this.resultBox.innerHTML += '<b>Result: </b>' + result["result"] + '<br>'
    this.resultBox.innerHTML += '<b>Iterations: </b>' + result["iterations"] + '<br>'
    this.resultBox.innerHTML += '<b>Status: </b>' + result["status"] + '<br>'
    this.resultBox.innerHTML += '<b>Head position: </b>' + result["head_position"] + '<br><br>'

    this.resultBox.innerHTML += '<b>Steps:</b><br>'

    let table = document.createElement('table')
    this.AddRowWithValues(table, ['curr state', 'curr char', 'next state', 'next char', 'move'], 'th')

    for (let i = 0; i < result["steps"].length; i++) {
        let step = result["steps"][i]
        let curr_state = step["curr_state"]
        let next_state = step["next_state"]
        let curr_char = step["curr_character"]
        let next_char = step["next_character"]
        let move = step["move"]

        this.AddRowWithValues(table, [curr_state, curr_char, next_state, next_char, move])
    }

    this.resultBox.appendChild(table)
}
