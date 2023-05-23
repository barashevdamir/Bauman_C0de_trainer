console.log('test')
let intervalId;
document.querySelectorAll('.filter__dropdown-btn').forEach(e=>{
  e.addEventListener('click', e =>{
    const menu = e.currentTarget.dataset.path;
    document.querySelectorAll('.filter__dropdown-menu').forEach(e=>{

      if (!document.querySelector(`[data-target=${menu}]`).classList.contains('open')){
        e.classList.remove('filter__dropdown-menu--active');
        document.querySelectorAll('.filter__dropdown-btn').forEach(e=>{
          e.classList.remove('filter__dropdown-btn--active');
        })
        e.classList.remove('open');
        document.querySelector(`[data-target=${menu}]`).classList.add('filter__dropdown-menu--active');
        document.querySelector(`[data-path=${menu}]`).classList.add('filter__dropdown-btn--active');
        intervalId = setTimeout(()=>{
          document.querySelector(`[data-target=${menu}]`).classList.add('open');
        }, 0)
      }
      if (document.querySelector(`[data-target=${menu}]`).classList.contains('open')) {
        clearTimeout(intervalId);
        document.querySelector(`[data-target=${menu}]`).classList.remove('filter__dropdown-menu--active');
        document.querySelector(`[data-path=${menu}]`).classList.remove('filter__dropdown-btn--active');
        document.querySelector(`[data-target=${menu}]`).classList.remove('filter__dropdown-menu--open');
        intervalId = setTimeout(()=>{
          document.querySelector(`[data-target=${menu}]`).classList.remove('open');
        }, 0)
      }
    })
  })
})