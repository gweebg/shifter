<script>
    import { page } from '$app/stores';
</script>

<div class="h-[100vh] flex flex-col justify-center items-center">

    <h1 class="text-magnum-500 text-9xl mb-2">{$page.status}</h1>
    <h2 class="text-magnum-100 text-2xl font-bold tracking-wide">{$page.error.message.toUpperCase()}</h2>

</div>

