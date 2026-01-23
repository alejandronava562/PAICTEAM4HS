const form = document.querySelector("#idea-form");
const projectInput = document.querySelector("#project");
const contextInput = document.querySelector("#context");
const ideasBtn = document.querySelector("#ideas-btn");
const ideasStatus = document.querySelector("#idea-status");
const ideasCard = document.querySelector("#ideas-card");
const ideasList = document.querySelector("#ideas-list");
const planBtn = document.querySelector("#plan-btn");
const planCard = document.querySelector("#plan-card");
const planGoal = document.querySelector("#plan-goal");
const planTimeline = document.querySelector("#plan-timeline");
const planSteps = document.querySelector("#plan-steps");
const planStatus = document.querySelector("#plan-status");
const ideaError = document.querySelector("#idea-error");


// helper to render ideas
const renderIdeas = (directions = []) => {
  ideasList.innerHTML = "";
  directions.forEach((idea) => {
    const li = document.createElement("li");
    const radio = document.createElement("input");
    radio.type = "radio";
    radio.name = "idea-choice";
    radio.value = idea.idea_num ?? "";
    radio.dataset.label = idea.label ?? "";
    radio.required = true;

    const num = document.createElement("span");
    num.className = "idea-number";
    num.textContent = idea.idea_num ?? "?";

    const text = document.createElement("div");
    text.innerHTML = `<strong>${idea.label ?? "Untitled"}</strong><br>${idea.description ?? ""}`;

    li.appendChild(radio);
    li.appendChild(num);
    li.appendChild(text);
    ideasList.appendChild(li);
  });
};

//helper to reset the plan UI
const resetPlanUI = () => {
  planGoal.textContent = "";
  planTimeline.textContent = "";
  planSteps.innerHTML = "";
  planStatus.textContent = "";
  planCard.classList.add("hidden");
};
//generates ideas when form is submitted
form.addEventListener('submit', async(e) => {
    e.preventDefault();
    ideasStatus.innerHTML = '<div class="loader"></div>Generating...';
    // FIXME: fix ideasbtn var reference
    ideasBtn.disabled = true;
    ideasCard.classList.add("hidden");
    ideaError.textContent = "";
    resetPlanUI();
    // builds payload and calls /ideas
    try {
    const payload = {
      project: projectInput.value.trim(),
      context: contextInput.value.trim(),
    };

    const res = await fetch("/ideas", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    //checking http errors, parses JSON
    if (!res.ok) {
      throw new Error(`Request failed: ${res.status}`);
    }

    const data = await res.json();
    const directions = data.directions || [];
    renderIdeas(directions);
    //depending on UI will show or hide results
    ideasCard.classList.toggle("hidden", directions.length === 0);
    ideasStatus.textContent = directions.length
      ? "Ideas generated below."
      : "No ideas returned.";
  } catch (err) {
    ideasStatus.textContent = `Error: ${err.message}`;
    ideasCard.classList.add("hidden");
  } finally {
    ideasBtn.disabled = false;
  }

});
// when the generate project plan button is pressed
planBtn.addEventListener("click", async () => {
  ideaError.textContent = "";
  const selected = document.querySelector('input[name="idea-choice"]:checked');
  if (!selected) {
    ideaError.textContent = "Select an idea first.";
    return;
  }
// prepare UI and payload
  planStatus.textContent = "Generating plan...";
  planBtn.disabled = true;
  planCard.classList.add("hidden");

  const payload = {
    project: projectInput.value.trim(),
    context: contextInput.value.trim(),
    chosen_idea_num: selected.value,
    chosen_label: selected.dataset.label || "",
  };

  //calls /plan and parses JSON
  try {
    const res = await fetch("/plan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error(`Request failed: ${res.status}`);
    const data = await res.json();
    const plan = data.plan || {};

    //renders the plan
    planGoal.textContent = plan.goal || "";
    planTimeline.textContent = plan.timeline_days ?? "";
    planSteps.innerHTML = "";
    (plan.steps || []).forEach((step) => {
      const li = document.createElement("li");
      li.innerHTML = `<strong>${step.step_number}. ${step.label}</strong><br>${step.instructions}`;
      planSteps.appendChild(li);
    });

    planCard.classList.remove("hidden");
    planStatus.textContent = "";
  } catch (err) {
    planStatus.textContent = `Error: ${err.message}`;
    planCard.classList.add("hidden");
  } finally {
    planBtn.disabled = false;
  }
});
