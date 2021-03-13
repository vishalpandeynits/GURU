function _(el){
    return document.getElementById(el)
}
$(window).on('load', function(){
    $('#status').fadeOut();
    $('#preloader').delay(150).fadeOut('slow');
})
$.ajaxSetup({
    headers: { "X-CSRFToken": '{{csrf_token}}' }
});

if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}

function openNav() {
    _("mySidenav").style.width = "295px";
}

function closeNav() {
    _("mySidenav").style.width = "0";
}

function on(el) {
    el.style.display = 'flex';
    document.body.classList.add("no-scroll");
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
    document.body.style.overflow='hidden';
}
function on_nav(el) {
    el.style.display = 'flex';
}
function off(el) {
    el.style.display= "none";
    document.body.classList.remove("no-scroll");
    document.body.style.overflowY='auto';
}
window.addEventListener('online', function(e) {
    swal({
        title: "Network Connectivity",
        text: "Network connection is restored.",
        icon: "success",
        button: "OK !",
      });
});

window.addEventListener('offline', function(e) {
    swal({
        title: "Network Connectivity",
        text: "Netwok Connection lost, Please coonect again to experience smooth interaction.",
        icon: "error",
        button: "OK !",
      });
});

"use strict";
(() => {
const modified_inputs = new Set;
const defaultValue = "defaultValue";
// store default values
addEventListener("beforeinput", (evt) => {
    const target = evt.target;
    if (!(defaultValue in target || defaultValue in target.dataset)) {
        target.dataset[defaultValue] = ("" + (target.value || target.textContent)).trim();
    }
});
addEventListener("input", (evt) => {
    const target = evt.target;
    let original;
    if (defaultValue in target) {
        original = target[defaultValue];
    } else {
        original = target.dataset[defaultValue];
    }
    if (original !== ("" + (target.value || target.textContent)).trim()) {
        if (!modified_inputs.has(target)) {
            modified_inputs.add(target);
        }
    } else if (modified_inputs.has(target)) {
        modified_inputs.delete(target);
    }
});
addEventListener("submit", () => {
    modified_inputs.clear();
});
addEventListener("beforeunload", (evt) => {
    if (modified_inputs.size) {
        const unsaved_changes_warning = "Changes you made may not be saved.";
        evt.returnValue = unsaved_changes_warning;
        return unsaved_changes_warning;
    }
});
})();