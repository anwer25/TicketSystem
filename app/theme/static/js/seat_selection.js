document.addEventListener("DOMContentLoaded", function () {

  document.addEventListener("keydown", function (e) {
    const focusedSeat = document.activeElement;
    if (!focusedSeat.classList.contains("seat-button")) return;

    const seatId = focusedSeat.getAttribute("data-seat-id");
    const allSeats = Array.from(document.querySelectorAll(".seat-button"));
    const currentIndex = allSeats.findIndex(
      (seat) => seat.getAttribute("data-seat-id") === seatId
    );

    if (e.key === "ArrowRight" && currentIndex < allSeats.length - 1) {
      allSeats[currentIndex + 1].focus();
      e.preventDefault();
    } else if (e.key === "ArrowLeft" && currentIndex > 0) {
      allSeats[currentIndex - 1].focus();
      e.preventDefault();
    } else if (e.key === "ArrowUp") {

      if (currentIndex >= 10) allSeats[currentIndex - 10].focus();
      e.preventDefault();
    } else if (e.key === "ArrowDown") {

      if (currentIndex < allSeats.length - 10)
        allSeats[currentIndex + 10].focus();
      e.preventDefault();
    } else if (e.key === "Enter" || e.key === " ") {
      focusedSeat.click();
      e.preventDefault();
    }
  });


  tippy(".seat-button", {
    content(reference) {
      return reference.getAttribute("title");
    },
    placement: "top",
    theme: "light",
    arrow: true,
  });
});
