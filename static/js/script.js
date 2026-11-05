async function loadStudents() {
    const response = await fetch("/students");
    const students = await response.json();
    const list = document.getElementById("studentList");
    list.innerHTML = "";
    students.forEach(function (student) {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${student.id}</td>
            <td></td>
            <td>${student.age}</td>
            <td>
                <button class="edit">Edit</button>
                <button class="delete">Delete</button>
            </td>
        `;

        row.children[1].textContent = student.name;

        row.querySelector(".edit").onclick = function () {
            editStudent(student.id, student.name, student.age);
        };

        row.querySelector(".delete").onclick = function () {
            deleteStudent(student.id);
        };
        list.appendChild(row);
    });
}

loadStudents();


// CREATE
document.getElementById("studentForm").onsubmit = async function (event) {
    event.preventDefault();
    const name = document.getElementById("name").value;
    const age = Number(document.getElementById("age").value);
    const response = await fetch("/students", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: name,
            age: age
        })
    });
    if (!response.ok) {
        alert("Could not add student");
        return;
    }
    this.reset();
    loadStudents();
};

// UPDATE
async function editStudent(id, oldName, oldAge) {
    const name = prompt("Enter new name:", oldName);
    if (name === null || name.trim() === "") {
        return;
    }

    const ageText = prompt("Enter new age:", oldAge);
    if (ageText === null || ageText.trim() === "") {
        return;
    }

    const age = Number(ageText);
    if (!Number.isInteger(age) || age < 1) {
        alert("Enter a valid age");
        return;
    }

    const response = await fetch("/students/"+ id, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: name.trim(),
            age: age
        })
    }); 

    if (!response.ok) {
        alert("Could not update student");
        return;
    }

    loadStudents();
}


// DELETE
async function deleteStudent(id) {
    if (!confirm("Delete this student?")) {
        return;
    }

    const response = await fetch("/students/" + id, {
        method: "DELETE"
    });

    if (!response.ok) {
        alert("Could not delete student");
        return;
    }

    loadStudents();
}
