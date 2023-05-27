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




document.querySelectorAll('.order_by').forEach(e=>{
  e.addEventListener('click', e=>{

    let url = window.location;
    let params = window
    .location
    .search
    .replace('?','')
    .split('&')
    
    if (params != 0) {
      params.forEach((item, i) => {
        if (item.slice(0,9) == 'order_by=') {
          params.splice(i,1)
        } 

      })
      params.push('order_by=' + e.target.id)
      url = url.origin + url.pathname + '?' + params.sort().reverse().join('&')
    } else if (params == 0) {
      url = url.origin + url.pathname + '?order_by=' + e.target.id
    }

    window.location.replace(url)
  })
})


document.querySelectorAll('.language').forEach(e=>{
  e.addEventListener('click', e=>{

    let url = window.location;
    let params = window
    .location
    .search
    .replace('?','')
    .split('&')
    
    if (params != 0) {
      params.forEach((item, i) => {
        if (item.slice(0,9) == 'language=') {
          params.splice(i,1)
        } 

      })
      params.push('language=' + e.target.id)
      url = url.origin + url.pathname + '?' + params.sort().reverse().join('&')
    } else if (params == 0) {
      url = url.origin + url.pathname + '?language=' + e.target.id
    }

    window.location.replace(url)
  })
})


document.querySelectorAll('.level').forEach(e=>{
  e.addEventListener('click', e=>{
    let url = window.location;
    let params = window
    .location
    .search
    .replace('?','')
    .split('&')
    
    if (params != 0) {
      params.forEach((item, i) => {
        if (item.slice(0,6) == 'level=') {
          params.splice(i,1)
        } 

      })
      params.push('level=' + e.target.id)
      url = url.origin + url.pathname + '?' + params.sort().reverse().join('&')
    } else if (params == 0) {
      url = url.origin + url.pathname + '?level=' + e.target.id
    }

    window.location.replace(url)
  })
})


document.querySelectorAll('.tag').forEach(e=>{
  e.addEventListener('click', e=>{

    let url = window.location;
    let params = window
    .location
    .search
    .replace('?','')
    .split('&')
    
    if (params != 0) {
      params.forEach((item, i) => {
        if (item.slice(0,4) == 'tag=') {
          params.splice(i,1)
        } 

      })
      params.push('tag=' + e.target.id)
      url = url.origin + url.pathname + '?' + params.sort().reverse().join('&')
    } else if (params == 0) {
      url = url.origin + url.pathname + '?tag=' + e.target.id
    }

    window.location.replace(url)
  })
})

document.querySelector('.filter__clear-btn').addEventListener('click', e => {
  let url = window.location;
  url = url.origin + url.pathname + ''
  window.location.replace(url)
})