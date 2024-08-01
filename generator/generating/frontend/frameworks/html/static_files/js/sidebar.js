const triggers = {}
const click = fn => document.addEventListener('click', fn)
click(e => Object.keys(triggers).forEach(x => e.target.matches(x) || e.target.closest(x) ? triggers[x](e) : null))
triggers['aside .parent>span'] = e => console.log(e)
