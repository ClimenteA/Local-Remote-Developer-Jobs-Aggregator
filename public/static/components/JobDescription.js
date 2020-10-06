function str_replace(e, t, n, i) {
    var r, o = 0, a = 0, s = "", l = "", c = 0, u = [].concat(e), d = [].concat(t), h = n, p = "[object Array]" === Object.prototype.toString.call(d), f = "[object Array]" === Object.prototype.toString.call(h);
    for (h = [].concat(h),
    i && (this.window[i] = 0),
    o = 0,
    r = h.length; o < r; o++)
        if ("" !== h[o])
            for (a = 0,
            c = u.length; a < c; a++)
                s = h[o] + "",
                l = p ? void 0 !== d[a] ? d[a] : "" : d[0],
                h[o] = s.split(u[a]).join(l),
                i && h[o] !== s && (this.window[i] += (s.length - h[o].length) / u[a].length);
    return f ? h : h[0]
}



function clean_description(raw_text){       
    if (raw_text.includes("markdown")){
        raw_text = str_replace("\\n", "\n", raw_text)
    }
    return m.trust("<div class='job-description' style='white-space: pre-line;'>" + raw_text + "</div>")
}


const JobDescription = () => {
    
    let show_description = false

    function toggle_description(event){
        show_description = !show_description
        event.target.parentElement.parentElement.scrollIntoView({behavior: "smooth"})
    }

    return {
        view: v => {

            let description = clean_description(v.attrs.description)

            return [
                m(`div.${show_description ? "is-block" : "is-hidden"}.mb-4`, description),            
                
                m("button.button.ml-3", 
                { onclick: ev => toggle_description(ev) }, 
                show_description ? "LESS" : "MORE" ),
            ]
        }
    }
}


export default JobDescription