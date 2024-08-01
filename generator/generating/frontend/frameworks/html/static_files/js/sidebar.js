const _ = (el, parent = document) => new S(el, parent)
class S {     /*SELECT*/
  constructor(el, parent = document) {  //Selector or DOM Element
    if (typeof el == 'string') this.el = parent.querySelector(el)
    else this.el = el;
    if (this.el) {
      this.cl = this.el.classList
      this.at = new Object()
      this.at.toggle = (attr) => this.el.toggleAttribute(attr)
      this._ = child => _(child, this.el)
      this.sibling = sibling => _(sibling, this.el.parentElement)
    }
  }
  click(triggers) {
    return new L(this.el, ['click'], triggers)
  }
}
class L {   /*LISTEN*/
  constructor(target, events = [], triggers = {}) {
    const listener = this
    listener.triggers = triggers;
    const fn = (e) => listener.listen(e)
    events.forEach((ev) => target.addEventListener(ev, fn))
  }
  listen(e) {
    const ev = new E(e)
    const triggers = this.triggers
    Object.keys(triggers).forEach(x => {
      const match = ev.extract(x)
      if (match) {
        const parent = match.parentElement
        triggers[x]({ parent, match })
      }
    })
  }
}
class E {  /*event*/
  constructor(e) {
    this.e = e
    this.tg = e.target || null
  }
  extract(selector) {
    if (!this.tg) return null;
    if (this.tg.matches(selector)) return this.tg;
    const closest = this.tg.closest(selector);
    if (closest) return closest
    else return null;
  }
}
_('aside').click({
  'aside .parent>div': ({ parent, match }) => {
    _(parent).cl.toggle('open')
    _(match).sibling('ul').at.toggle('hidden')
  }
})
