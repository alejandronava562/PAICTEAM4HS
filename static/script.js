const form = document.querySelector("#idea-form")
const project_input = document.querySelector("#project")
const context_input = document.querySelector("#context")
const ideasBtn = document.querySelector("#ideas-btn")
const ideasStatus = document.querySelector("#idea-status")

form.addEventListener('submit', async(e) => {
    e.preventDefault();
    ideasStatus.textContent="Generating...";
    // FIXME: fix ideasbtn var reference
    ideasBtn.disabled = true;
    // TODO : CALL /idea flask endpoint
})