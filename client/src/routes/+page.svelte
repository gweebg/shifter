<script>
// @ts-nocheck


    import Calendar from "@event-calendar/core";
    import TimeGrid from "@event-calendar/time-grid";
    import '@event-calendar/core/index.css';

    let startingDate = new Date();
    startingDate.setHours(9, 0);

    let endingDate = new Date();
    endingDate.setHours(11, 0);
    
    const formatTime = (/** @type {string} */ time) => {
        const date = new Date(time);
        const hours = date.getHours().toString().padStart(2, '0'); // Ensure two-digit hours
        const minutes = date.getMinutes().toString().padStart(2, '0'); // Ensure two-digit minutes
        return `${hours}:${minutes}`;
    }

    const myEvents = [
        {
            id: "event_a",
            allDay: false,
            start: startingDate,
            end: endingDate,
            title: "Este é o meu evento.",
            display: "auto",
            backgroundColor: "pink",
            textColor: "black"
        },
        {
            id: "event_b",
            allDay: false,
            start: startingDate,
            end: endingDate,
            title: "Este é o meu evento 2.",
            display: "auto",
            textColor: "white"
        }
    ]

    let plugins = [TimeGrid];
    let options = {
        view: "timeGridWeek",
        events: [...myEvents],
        date: new Date(),
        slotDuration: "01:00",
        dayHeaderFormat: {weekday: "long"},
        firstDay: 1,
        allDaySlot: false,
        slotMinTime: "08:00",
        slotMaxTime: "20:00",
        slotLabelFormat: formatTime,
        height: "100%",
        slotHeight: 70,
        height: "100%",
        hiddenDays: [0],
        headerToolbar: {start: '', center: '', end: ''}
    }

</script>


<div class="main">

    <div class="bar">
        Ola
    </div>
    <div class="cal">
        <Calendar {plugins} {options}/>
    </div>

</div>


<style>

    .main {
        height: 100%;
        width: 100%;
        display: flex;
        flex-direction: row;
    }

    .cal {
        width: 80%;
        margin: 20px;
    }

    .bar {
        width: 20%;
        background-color: bisque;
    }

    :global(.ec) {
        font-family:'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
    }

    :global(.ec-time, .ec-line) {
        height: 70px;  
    }

    :global(.ec-header) {
        border-radius: 10px 10px 0 0;
    }

    :global(.ec-event) {
        padding: 10px;
        border-radius: 10px;
        width: 100%;
        margin-left: 3px;
    }

    :global(.ec-body.ec-compact) {
        border-radius: 0 0 10px 10px;
    }


</style>