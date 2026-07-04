

// ====================== BOOKING MODAL ======================

const modal = document.getElementById("bookingModal");

let selectedConcertId = 0;
let selectedConcertPrice = 0;

function openBooking(concertId, concertName) {

    selectedConcertId = concertId;

    console.log("Selected Concert ID:", selectedConcertId);

    document.getElementById("concertSelect").value = concertName;

    modal.style.display = "flex";
}

function closeBooking() {

    modal.style.display = "none";

    document.getElementById("bookingForm").reset();

    selectedConcertId = 0;
    selectedConcertPrice = 0;
}

// Close modal when clicking outside
window.onclick = function(event) {

    if (event.target == document.getElementById("bookingModal")) {
        closeBooking();
    }

    if (event.target == document.getElementById("paymentModal")) {
        closePaymentModal();
    }

}
// ====================== BOOKING FORM ======================

document.getElementById("bookingForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const phone = document.getElementById("phone").value;
    const concert = document.getElementById("concertSelect").value;

    if (!selectedConcertId) {
        alert("Please select a concert.");
        return;
    }

    const bookingData = {
        username: name,
        email: email,
        phone_number: phone,
        concerttable_id: Number(selectedConcertId),
        booking_status: "Booked"
    };

    const response = await fetch("http://127.0.0.1:8000/user-booking/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(bookingData)
    });

    const result = await response.json();

    if (!response.ok) {
        alert(result.detail || "Booking Failed");
        return;
    }

    const bookingId = result.booking.id;

    document.getElementById("profileName").innerText = name;
    document.getElementById("profileEmail").innerText = email;
    document.getElementById("profilePhone").innerText = phone;
    document.getElementById("profileConcert").innerText = concert;
    document.getElementById("bookingStatus").innerHTML = "✅ Booked";
    document.getElementById("profilePayment").innerText = "Pending";

    alert("🎉 Booking Successful!");

    document.getElementById("bookingForm").reset();

    closeBooking();          // Close booking popup

    openPaymentModal(concert, bookingId);   // Open payment popup
});

function openPaymentModal(concertName, bookingId) {

    // Reset payment form
    document.getElementById("transactionId").value = "";
    document.getElementById("paymentMethod").selectedIndex = 0;

    document.getElementById("payConcertName").value = concertName;

    document.getElementById("paymentModal").style.display = "flex";

    window.currentBookingId = bookingId;
}
function closePaymentModal() {

    document.getElementById("paymentModal").style.display = "none";

    document.getElementById("transactionId").value = "";
    document.getElementById("paymentMethod").selectedIndex = 0;
    document.getElementById("payConcertName").value = "";
}
function showSection(sectionId, element) {

    document.querySelectorAll(".page").forEach(page => {
        page.classList.remove("active");
    });

    document.getElementById(sectionId).classList.add("active");

    document.querySelectorAll(".nav-link").forEach(link => {
        link.classList.remove("active");
    });

    if (element) {
        element.classList.add("active");
    }

    closeMenu();

}

function toggleMenu() {
    document.getElementById("navMenu").classList.toggle("show");
}

function closeMenu() {
    document.getElementById("navMenu").classList.remove("show");
}
async function loadConcerts() {

    try {

        const response = await fetch("http://127.0.0.1:8000/concerts/");

        if (!response.ok) {
            throw new Error("Failed to fetch concerts");
        }

        const concerts = await response.json();
        const select = document.getElementById("concertSelect");

        select.innerHTML = '<option value="">Select Concert</option>';

        concerts.forEach(concert => {
            select.innerHTML += `
        <option value="${concert.concert_name}">
            ${concert.concert_name}
        </option>
    `;
        });

        const container = document.getElementById("concertContainer");



        container.innerHTML = "";

        concerts.forEach(concert => {

            console.log(concert);
            console.log("ID =", concert.id);
            let image = "";

            switch (concert.concert_name) {

                case "Rock Night":
                    image = "images/rock.jpg";
                    break;

                case "Summer Beats":
                    image = "images/summer.jpg";
                    break;

                case "Music Fest":
                    image = "images/musicfest.jpg";
                    break;

                case "Live Concert":
                    image = "images/live.jpg";
                    break;

                

                default:
                    image = "images/default.jpg";
            }

            container.innerHTML += `
        <div class="card">

            <img src="${image}" alt="${concert.concert_name}">

            <h2>${concert.concert_name}</h2>

            <p><b>Artist :</b> ${concert.artist_name}</p>

            <p><b>Venue :</b> ${concert.venue}</p>

            <p><b>Date :</b> ${concert.concert_date}</p>

            <p><b>Price :</b> ₹${concert.ticket_price}</p>

            <button class="book-btn"
    data-id="${concert.id}"
    data-name="${concert.concert_name}"
    data-price="${concert.ticket_price}">
    Book Now
</button>
        </div>
    `;

        });

    }
    catch (error) {

        console.error(error);

        alert("Unable to load concerts");

    }

}
document.addEventListener("click", function (e) {

    if (e.target.classList.contains("book-btn")) {

        selectedConcertId = Number(e.target.dataset.id);
        selectedConcertPrice = Number(e.target.dataset.price);

        document.getElementById("concertSelect").value = e.target.dataset.name;

        document.getElementById("bookingModal").style.display = "flex";
    }
});


// ====================== PROFILE LOAD ======================
async function loadProfile() {

    const response = await fetch("http://127.0.0.1:8000/user-booking/");
    const data = await response.json();
    console.log(data);
    if (data.length === 0) return;

    const latest = data[data.length - 1];

    document.getElementById("profileName").innerText = latest.username;
    document.getElementById("profileEmail").innerText = latest.email;
    document.getElementById("profilePhone").innerText = latest.phone_number;

    document.getElementById("bookingStatus").innerText = "Booked";
    document.getElementById("profileConcert").innerText = latest.concert_name;
}




async function confirmPayment() {

    const transactionId = document.getElementById("transactionId").value;
    const paymentMethod = document.getElementById("paymentMethod").value;

    if (!transactionId || !paymentMethod) {
        alert("Please fill all payment details");
        return;
    }

    const response = await fetch("http://127.0.0.1:8000/payments/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            bookingtable_id: window.currentBookingId,
            amount: selectedConcertPrice,
            payment_method: paymentMethod,
            transaction_id: transactionId
        })
    });

    const result = await response.json();
    console.log(result);

    if (!response.ok) {
        alert(result.detail || "Payment Failed");
        return;
    }

    alert("✅ Payment Successful!");

closePaymentModal();

await generateTicket(window.currentBookingId);

showSection("profile");
}
window.onload = function () {
    loadConcerts();
    loadProfile();
};