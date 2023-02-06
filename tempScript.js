const fs = require("fs")

let modules = [
    "WM160",
    "WM161",
    "WM162",
    "WM163"
]


const generateRandomNumber = (min, max) => {
    return Math.floor(Math.random() * (max - min + 1) + min)
}

let data = Array(100).fill(0).map((a, index) => {
    return {
        student_id: index,
        results: modules.map(m => {
            return {
                module: m,
                quiz_mark: generateRandomNumber(50, 100),
                module_mark: generateRandomNumber(50, 100)
            }
        })
    }
})

fs.writeFileSync('data.json', JSON.stringify(data, null, 4));