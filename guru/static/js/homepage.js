function _(el){
    return document.getElementById(el)
}

if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}

function openNav() {
    _("mySidenav").style.width = "295px";
}

function closeNav() {
    _("mySidenav").style.width = "0";
}

function createclassform() {
    if (_('classform').style.display == 'none') {
        _('joinform').style.display = 'none';
        _('classform').style.display = 'block';
    } else {
        _('classform').style.display = 'none'
    }
}

function joinform() {
    if (display == _('joinform').style.display == 'none') {
        _('classform').style.display = 'none'
        _('joinform').style.display = 'block';
    } else {
        _('joinform').style.display = 'none';
    }
}

// POLL JS
function addInputField(){
    _('more-inputs').innerHTML += '<input type="text" autocomplete="off" class="new" placeholder="Mention your option..." name="check">'
    new_inputs = document.getElementsByClassName('new')
    new_inputs[new_inputs.length-1].focus()

}

function toggleFlexForm(x){
    x.style.display=x.style.display=='none'?'flex':'none';
}

function toggleBlockForm(x){
    if (!x.style.display || x.style.display == "none") {
        x.style.display = "block";
    }
    else {
        x.style.display = "none";
    }
}  

//EMPTY COMMENT ISSUE
function checkComment(){
    var value=_('id_comment').value
    value = value.trim()
    if(value.length==0){
        _('id_submit').disabled=true;
    }
    else{
        _('id_submit').disabled=false;
    }
}

//EMPTY COMMENT ISSUE ENDS

//HOMEPAGE JAVASCRIPT
function on(el) {
    el.style.display = "flex";
}

function off(el) {
    el.style.display= "none";
}
function toggleMembersSubjects(){
    console.log(_('members'))
    _('members').style.display = _('members').style.display==='block'?'none':'block';
    _('activity').style.display = _('members').style.display==='block'?'none':'block';
}