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

// POLL JS
function addInputField(){
    var container = document.getElementById("more-inputs");
    var input = document.createElement("input");
    input.type = "text";
    input.name = "check";
    input.placeholder = "Mention your option."
    container.appendChild(input)
    input.focus();
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
    el.style.display = 'flex';
    document.body.classList.add("no-scroll");
}
function off(el) {
    el.style.display= "none";
    document.body.classList.remove("no-scroll");
}

function toggleMembersSubjects(){  
    _('members').style.display = _('members').style.display==='block'?'none':'block';
    _('activitya').style.display = _('members').style.display==='block'?'none':'block';
}


$(document).ready(function() {
    $('#close-btn').click(function() {
    $('#search-overlay').slideUp(200);
    $('#search-btn').show();
});
$('#search-btn').click(function() {
    $(this).hide();
    $('#search-overlay').slideDown(200);
});
});

$(document).on('click', function (e) {
    if ($(e.target).closest("#search-overlay").length === 0  ) {
        if(e.target!== _('search-btn' )){
            $("#search-overlay").slideUp(200);
            $('#search-btn').show();
        }    
    }
});

function deleteConfirm(entity, successCallback){
    var modal = $('#genericDeleteModal');
    modal.find('.modal-body .entityType').html(entity);
    modal.modal('show')
    $('#confirmDeleteButton').bind('click', function() 
    {
      var deleteTextInput = modal.find('#deleteConfirmText');
      if(deleteTextInput.val() === 'Delete'){
        modal.modal('hide');
        successCallback();
      }
    })
};

$('#genericDeleteModal').on('hide.bs.modal',function(){
    var modal = $(this);
    var deleteTextInput = modal.find('#deleteConfirmText');
    deleteTextInput.val('');
});

//Local delete button callback
$('#userDeleteButton').on('click',function(){
var entity = $('#SelectedUser').val();
deleteConfirm(entity,myRandomSuccessCallBackFunction)
});

//local success callback after delete function
function myRandomSuccessCallBackFunction()
{
    url =_('userDeleteButton').value
    window.location.href = 'http://127.0.0.1:8000'+url
}

function show_all_submissions(){
    $('#all_submissions').show()
    $('#ontime').hide()
    $('#late_submissions').hide()
    $('#not_submitted').hide()
}
function show_ontime_submissions(){
    $('#all_submissions').hide()
    $('#ontime').show()
    $('#late_submissions').hide()
    $('#not_submitted').hide()
}
function show_late_submissions(){
    $('#all_submissions').hide()
    $('#ontime').hide()
    $('#late_submissions').show()        
    $('#not_submitted').hide()
}
function show_not_submitted(){
    $('#all_submissions').hide()
    $('#ontime').hide()
    $('#late_submissions').hide()
    $('#not_submitted').show()
}
function cl(){
    $('#all_submissions').hide()
    $('#ontime').hide()
    $('#late_submissions').hide()
    $('#not_submitted').hide()
}

function copyText(text) {
    navigator.clipboard.writeText(text);
}
function myFunction() {
    var copyext = document.getElementById("classroom-code").textContent;
    copyText(copyext); 

    var tooltip = document.getElementById("myTooltip");
    tooltip.innerHTML = "Copied: " + copyext;
}
function outFunc() {
    var tooltip = document.getElementById("myTooltip");
    tooltip.innerHTML = "Copy to clipboard";
}

document.body.addEventListener('click',(e)=>{
    if(e.target != document.getElementById('co') && e.target != document.getElementById('left') && e.target != document.getElementById('icon')){
        document.getElementById('dropdown-container').style.display=null;
        document.body.classList.remove("no-scroll");
    }
})