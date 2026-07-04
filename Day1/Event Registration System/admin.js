// ====================== PAGE NAVIGATION ======================
function showPage(pageId) {

    let pages = document.querySelectorAll(".page");

    pages.forEach(page => {
        page.classList.remove("active");
    });

    document.getElementById(pageId).classList.add("active");
}

// ====================== MODALS ======================

const concertModal = document.getElementById("concertModal");
const viewModal = document.getElementById("viewModal");
const userViewModal = document.getElementById("userViewModal")
const userEditModal = document.getElementById("userEditModal");
const userDeleteModal = document.getElementById("userDeleteModal");
const deleteModal = document.getElementById("deleteModal");
function closeUserEditModal() {
    userEditModal.style.display = "none";
}
// Open Add/Edit Modal
let editingConcertId = null;
function openConcertModal() {

    editingConcertId = null;

    document.getElementById("modalTitle").innerText = "Add Concert";
    document.getElementById("userForm").addEventListener("submit", async function (e) {

    });
    document.getElementById("concertForm").reset();

    concertModal.style.display = "flex";
}

// Close Add/Edit Modal
function closeConcertModal() {
    concertModal.style.display = "none";
}

// Open View Modal
function viewConcert() {
    viewModal.style.display = "flex";
}

// Close View Modal
function closeViewModal() {
    viewModal.style.display = "none";
}
function closeUserViewModal() {
    userViewModal.style.display = "none";
}
// Open Delete Modal
function deleteConcert() {
    deleteModal.style.display = "flex";
}

// Close Delete Modal
function closeDeleteModal() {
    deleteModal.style.display = "none";
}
function closeUserDeleteModal() {
    userDeleteModal.style.display = "none";
}
// Close modal when clicking outside
window.onclick = function (event) {

    if (event.target == concertModal) {
        closeConcertModal();
    }

    if (event.target == viewModal) {
        closeViewModal();
    }

    if (event.target == deleteModal) {
        closeDeleteModal();
    }

    if (event.target == userViewModal) {
        closeUserViewModal();
    }

    if (event.target == userEditModal) {
        closeUserEditModal();
    }

    if (event.target == userDeleteModal) {
        closeUserDeleteModal();
    }

    if (event.target == document.getElementById("successModal")) {
        closeSuccessModal();
    }
};


function toggleSidebar() {
    document.querySelector(".sidebar").classList.toggle("active");
}


function showSection(pageId, element) {

    console.log("Clicked:", pageId);

    document.querySelectorAll(".page").forEach(page => {
        page.classList.remove("active");
    });

    const section = document.getElementById(pageId);

    console.log(section);

    if (!section) {
        alert(pageId + " section not found!");
        return;
    }

    section.classList.add("active");

    document.querySelectorAll(".menu a").forEach(link => {
        link.classList.remove("active");
    });

    element.classList.add("active");
}
function toggleSidebar() {
    document.getElementById("sidebar").classList.toggle("show");
}

function closeSidebar() {
    if (window.innerWidth <= 768) {
        document.getElementById("sidebar").classList.remove("show");
    }
}


// ====================== ADD / EDIT CONCERT ======================

document.getElementById("concertForm").addEventListener("submit", async function (e) {

    e.preventDefault();

    const inputs = this.querySelectorAll("input");

    const concertData = {
        concert_name: inputs[0].value,
        artist_name: inputs[1].value,
        venue: inputs[2].value,
        concert_date: inputs[3].value,
        total_seats: parseInt(inputs[4].value),
        ticket_price: parseFloat(inputs[5].value)
    };

    try {

        let response;

        // ---------- EDIT ----------
        if (editingConcertId !== null) {

            response = await fetch(
                `http://127.0.0.1:8000/concerts/${editingConcertId}`,
                {
                    method: "PATCH",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(concertData)
                }
            );

            if (!response.ok) {
                const error = await response.json();
                console.log(error);
                alert(error.detail);
                return;
            }

            alert("Concert Updated Successfully!");

        }

        // ---------- ADD ----------
        else {

            response = await fetch(
                "http://127.0.0.1:8000/concerts/",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(concertData)
                }
            );

            if (!response.ok) {
                throw new Error("Add failed");
            }

            alert("Concert Added Successfully!");
        }

        closeConcertModal();

        editingConcertId = null;

        this.reset();

        loadConcertData();

        loadDashboard();

    }

    catch (error) {

        console.error(error);

        alert("Operation Failed");

    }

});
// ====================== EDIT ======================

let currentRow = null;
function editConcert(id) {

    const concert = concerts.find(c => c.id == id);

    if (!concert) {
        alert("Concert not found");
        return;
    }

    editingConcertId = concert.id;

    document.getElementById("modalTitle").innerText = "Edit Concert";

    const inputs = document.querySelectorAll("#concertForm input");

    inputs[0].value = concert.concert_name;
    inputs[1].value = concert.artist_name;
    inputs[2].value = concert.venue;
    inputs[3].value = concert.concert_date;
    inputs[4].value = concert.total_seats;
    inputs[5].value = concert.ticket_price;

    concertModal.style.display = "flex";
}


// ====================== DELETE ======================



let deleteRowReference = null;

function deleteRow(button) {

    deleteRowReference = button.parentElement.parentElement;

    deleteModal.style.display = "flex";

}

document.querySelector(".delete-btn").onclick = async function () {

    if (deleteRowReference) {

const concertId = deleteRowReference.dataset.id;
        try {

            const response = await fetch(`http://127.0.0.1:8000/concerts/${concertId}`, {

                method: "DELETE"

            });

            if (!response.ok) {
                throw new Error("Failed to delete concert");
            }

            deleteRowReference.remove();

            alert("Concert Deleted Successfully!");

            deleteModal.style.display = "none";

            deleteRowReference = null;

        }
        catch (error) {

            console.error(error);

            alert("Error deleting concert!");

        }

    }

};



let users = [];

function loadUsers() {

    const table = document.getElementById("userTable");

    if (!table) return;

    table.innerHTML = "";

    users.forEach((user, index) => {

        table.innerHTML += `
        <div class="info-card">

            <h3>${user.username}</h3>

            <p><b>Email:</b> ${user.email}</p>

            <p><b>Phone:</b> ${user.phone_number}</p>

            <div class="card-actions">

                <button class="edit" onclick="editUser(${index})">
                    <i class="fa-solid fa-pen"></i>
                </button>

                <button class="delete" onclick="deleteUser(${index})">
                    <i class="fa-solid fa-trash"></i>
                </button>

            </div>

        </div>`;
    });

}

async function fetchUsers() {
    try {
        const response = await fetch("http://127.0.0.1:8000/users/");

        if (!response.ok) {
            throw new Error("Failed to fetch users");
        }

        users = await response.json();
        console.log(users); // 👈 store data here
        loadUsers(); // 👈 render table

    } catch (error) {
        console.error("Error:", error);
        alert("Failed to load users.");
    }
}

// ====================== USER VIEW ======================


async function viewUser(index) {
    try {
        const user = users[index];

        if (!user) {
            throw new Error("User not found");
        }

        document.getElementById("viewUserId").innerText = user.id;
        document.getElementById("viewUserName").innerText = user.username;
        document.getElementById("viewUserEmail").innerText = user.email;
        document.getElementById("viewUserPhone").innerText = user.phone_number;

        userViewModal.style.display = "flex";

    } catch (error) {
        console.error("Error:", error);
        alert("Failed to load user details.");
    }
}
// ====================== USER EDIT ======================
let editingUserId = null;

async function editUser(index) {

    try {

        const user = users[index];

        if (!user) {
            throw new Error("User not found");
        }

        // Store user id for update
        editingUserId = user.user_id;   // If this doesn't work, use user.id

        document.getElementById("editUserName").value = user.username;
        document.getElementById("editUserEmail").value = user.email;
        document.getElementById("editUserPhone").value = user.phone_number;

        userEditModal.style.display = "flex";

    } catch (error) {

        console.error(error);
        alert("Failed to load user.");

    }

}
document.getElementById("userForm").addEventListener("submit", async function (e) {

    e.preventDefault();

    const userData = {
        username: document.getElementById("editUserName").value,
        email: document.getElementById("editUserEmail").value,
        phone_number: document.getElementById("editUserPhone").value
    };

    try {

        const response = await fetch(
            `http://127.0.0.1:8000/users/${editingUserId}`,
            {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(userData)
            }
        );

        if (!response.ok) {
            const error = await response.json();
            alert(error.detail);
            return;
        }

        alert("User Updated Successfully!");

        closeUserEditModal();

        fetchUsers();

    } catch (error) {

        console.error(error);
        alert("Update Failed");

    }

});

// ====================== LOAD CONCERTS ======================

function deleteUser(index) {

    console.log("Index:", index);
    console.log("Users Array:", users);
    console.log("Selected User:", users[index]);

    currentUserId = users[index].user_id;

    console.log("Current User ID:", currentUserId);

    userDeleteModal.style.display = "flex";
}

document.getElementById("confirmUserDelete").onclick = async function () {

    try {

        console.log("Deleting User ID:", currentUserId);

        const response = await fetch(
            `http://127.0.0.1:8000/users/${currentUserId}`,
            {
                method: "DELETE"
            }
        );

        if (!response.ok) {
            throw new Error("Failed to delete user");
        }

        closeUserDeleteModal();

        fetchUsers();

        alert("User Deleted Successfully!");

    }
    catch (error) {
        console.error(error);
        alert("Failed to delete user.");
    }

};

async function loadConcertData(id = "") {

    const table = document.getElementById("concertTable");

    if (!table) return;

    table.innerHTML = "";

    try {

        let url = "http://127.0.0.1:8000/concerts/";

        if (id !== "") {
            url += `?id=${id}`;
        }

        const response = await fetch(url);

        if (!response.ok) {
            throw new Error("Failed to fetch concerts");
        }

concerts = await response.json();

const concertList = Array.isArray(concerts) ? concerts : [concerts];
        
        concertList.forEach(concert => {

            
            table.innerHTML += `
<div class="info-card" data-id="${concert.id}">
    <h3>${concert.concert_name}</h3>

    <p><b>Artist:</b> ${concert.artist_name}</p>
    <p><b>Venue:</b> ${concert.venue}</p>
    <p><b>Date:</b> ${concert.concert_date}</p>
    <p><b>Seats:</b> ${concert.total_seats}</p>
    <p><b>Price:</b> ₹${concert.ticket_price}</p>

    <div class="card-actions">
    <button class="edit" onclick="editConcert(${concert.id})">
            <i class="fa-solid fa-pen"></i>
        </button>

        <button class="delete" onclick="deleteRow(this)">
            <i class="fa-solid fa-trash"></i>
        </button>
    </div>
</div>
`;
        });

    } catch (error) {
        console.error(error);
        alert("Error loading concert data!");
    }

}


async function loadBookings() {

    console.log("loadBookings called");

    const table = document.getElementById("bookingTable");

    if (!table) return;

    table.innerHTML = "";

    try {

        const response = await fetch("http://127.0.0.1:8000/user-booking/");

        if (!response.ok) {
            throw new Error("Failed to fetch bookings");
        }

        const bookings = await response.json();

        console.log(bookings);

    

    bookings.forEach((booking) => {

    table.innerHTML += `
    <div class="info-card">

        <h3>${booking.username}</h3>

        <p><b>Email:</b> ${booking.email}</p>

        <p><b>Concert:</b> ${booking.concert_name}</p>

        <p><b>Status:</b> ${booking.booking_status}</p>

        <div class="card-actions">

            ${
                booking.booking_status === "Booked"
                ? `
                <button class="edit"
                    onclick="sendTicket(${booking.id})">
                    Send Ticket
                </button>
                `
                : `<span style="color:green;font-weight:bold;">✔ Ticket Sent</span>`
            }

        </div>

    </div>
    `;
});
     } catch (error) {
        console.error(error);
        alert("Failed to load bookings!");
    }
}
// 👇 ADD THIS HERE
async function sendTicket(bookingId) {

    try {

        const response = await fetch(
            `http://127.0.0.1:8000/user-booking/${bookingId}/send-ticket`,
            {
                method: "PATCH"
            }
        );

        const data = await response.json();

        if (!response.ok) {
            alert(data.detail);
            return;
        }

        alert(data.message);

        // Refresh the booking table
        loadBookings();

    } catch (error) {

        console.error(error);
        alert("Failed to send ticket.");

    }

}




async function loadDashboard() {

    try {

        // Total Users
        const userResponse = await fetch("http://127.0.0.1:8000/users/");
        const users = await userResponse.json();
        document.getElementById("userCount").innerText = users.length;

        // Total Concerts
        const concertResponse = await fetch("http://127.0.0.1:8000/concerts/");
        const concerts = await concertResponse.json();
        document.getElementById("concertCount").innerText = concerts.length;

        // Total Bookings
        const bookingResponse = await fetch("http://127.0.0.1:8000/user-booking/");
        const bookings = await bookingResponse.json();
        document.getElementById("bookingCount").innerText = bookings.length;

    } catch (error) {

        console.error(error);
        alert("Failed to load dashboard.");

    }

}



// ====================== INITIAL LOAD ======================

window.addEventListener("load", function () {

    // loadUsers();
    fetchUsers();
    loadConcertData();

    loadBookings();

    loadDashboard();

});

