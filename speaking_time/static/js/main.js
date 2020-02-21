function postStatus(taskID, data){
    $.ajax({
        url: `/${taskID}`,
        method:'POST',
        data: data
    });
}
function getStatus(taskID) {
  $.ajax({
    url: `/tasks/${taskID}`,
    method: 'GET'
  })
  .done((res) => {
    const taskData = `
      <tr id=${res.task_id}>
        <td>${res.file_id}</td>
        <td>${res.prog}</td>
        <td>${res.task_status}</td>
        <td>${res.per_fem}</td>
      </tr>`
//    var elem = document.getElementById(${res.task_id})
    if ( $("#" + res.task_id).length )
    {
        $("#" + res.task_id).replaceWith(taskData);
    } else {
        $("#tasks").prepend(taskData);
    }

//    $('#tasks').prepend(html);
    const taskStatus = res.task_status;
    if (taskStatus === 'finished' || taskStatus === 'failed') return false;
    setTimeout(function() {
      getStatus(res.task_id);
    }, 1000);
  })
  .fail((err) => {
    console.log(err)
  });
}


$(document).ready(function() {

    $('#submit').on('click', function(event) {
        event.preventDefault();
        var formData = new FormData($('form')[0]);
        $('#ProgressText').remove();
        $.ajax({
            xhr: function(){
                var xhr = new window.XMLHttpRequest();
                xhr.upload.addEventListener('progress', function(e) {
                    if (e.lengthComputable){
                        var percent = Math.round((e.loaded / e.total) * 100);
                        $('#InitProgress').attr('aria-valuenow', percent).css('width', percent + '%').text(percent + '%');
                    }
                });
                return xhr;
            },
            url: $SCRIPT_ROOT + "/_run_task",
            data: formData,
            method: "POST",
            processData: false,
            contentType: false
//            success: function() {
                //alert("File uploaded");
//                }
        })
		.done((res) => {
            if (!$('#taskTable').length){
                $('#FullBody').after(taskTable)
            }
			getStatus(res.task_id)
		});    
    });
});

const taskTable=`
<div id="taskTable">
    <h3>Task Status </h3><br>
    <table class="table">
      <thead>
        <tr>
          <th>File</th>
          <th>Progress</th>
          <th>Job Status</th>
          <th>Percentage female speech</th>
        </tr>
      </thead>
      <tbody id="tasks"></tbody>
    </table>
</div>`;
