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

function add_param(e, filter_name) {

  filter_name = filter_name + '='
  let url = window.location;
  let params = window
  .location
  .search
  .replace('?','')
  .split('&')
  
  if (params != 0) {
    params.forEach((item, i) => {
      if (item.slice(0,filter_name.length) == filter_name) {
        params.splice(i,1)
      } 
    })

    params.push(filter_name + e.target.id)
    url = url.origin + url.pathname + '?' + params.sort().reverse().join('&')
  } else if (params == 0) {
    url = url.origin + url.pathname + '?' + filter_name + e.target.id
  }

  window.location.replace(url)
}

function changeName(){
  let dropdownBtn = document.querySelectorAll('.filter__dropdown-btn')
  let params = window
  .location
  .search
  .replace('?','')
  .split('&')
  if (params != 0) {
    params.forEach((item, i) => {
      if (item.length >= 8) {
        if (item.slice(0,8) == 'order_by') {
          if (item.slice(9,) == '-create_datetime') {
            dropdownBtn[0].innerHTML = 'Newest'
          } 
          else if (item.slice(9,) == 'create_datetime') {
            dropdownBtn[0].innerHTML = 'Oldest'
          }
          else if (item.slice(9,) == '-solved') {
            dropdownBtn[0].innerHTML = 'Most Completed'
          }
          else if (item.slice(9,) == '-positive_rate') {
            dropdownBtn[0].innerHTML = 'Hight Rate'
          }
        }
      }
      if (item.length >= 8){
        if (item.slice(0,8) == 'language') {
          dropdownBtn[1].innerHTML = item.slice(9,)
        }
      }
      if (item.length >= 5){
        if (item.slice(0,5) == 'level') {
          dropdownBtn[2].innerHTML = "<span>lvl" + item.slice(6,) + "</span>"
        }
      }
      if (item.length >= 3){
        if (item.slice(0,3) == 'tag') {
          dropdownBtn[3].innerHTML = item.slice(4,)
        }
      }
    })
  }
}

changeName()


document.querySelectorAll('.order_by').forEach(e=>{
  e.addEventListener('click', e=>{
    add_param(e, 'order_by')
  })
})


document.querySelectorAll('.language').forEach(e=>{
  e.addEventListener('click', e=>{
    add_param(e, 'language')
  })
})


document.querySelectorAll('.level').forEach(e=>{
  e.addEventListener('click', e=>{
    add_param(e, 'level')
  })
})


document.querySelectorAll('.tag').forEach(e=>{
  e.addEventListener('click', e=>{
    add_param(e, 'tag')
  })
})


document.querySelector('.filter__clear-btn').addEventListener('click', e => {
  let url = window.location;
  url = url.origin + url.pathname + ''
  window.location.replace(url)
})