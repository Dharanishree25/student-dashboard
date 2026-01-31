function show(id) {
    document.querySelectorAll('.section').forEach(s => s.style.display='none');
    document.getElementById(id).style.display='block';
}

function addStudent() {
    fetch('/add_student', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({
            name: name.value,
            email: email.value,
            course: course.value,
            age: age.value
        })
    }).then(() => load());
}

function load() {
    fetch('/students')
    .then(r=>r.json())
    .then(data=>{
        let rows='';
        data.forEach(s=>{
            rows+=`
            <tr>
                <td>${s.id}</td>
                <td>${s.name}</td>
                <td>${s.email}</td>
                <td>${s.course}</td>
                <td>${s.age}</td>
                <td><button onclick="del(${s.id})">Delete</button></td>
            </tr>`;
        });
        table.innerHTML=rows;
    });
}

function del(id) {
    fetch('/delete/'+id,{method:'DELETE'}).then(()=>load());
}

function updateStudent() {
    fetch('/update_student', {
        method:'PUT',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({
            id: uid.value,
            name: uname.value,
            email: uemail.value,
            course: ucourse.value,
            age: uage.value
        })
    }).then(()=>load());
}

load();
