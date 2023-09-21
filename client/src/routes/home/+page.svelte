<script>


    import SearchForm from "$lib/components/home/SearchForm.svelte";

    export let data;

</script>

<main class="flex w-full justify-center items-center h-[100vh] flex-col">

    <SearchForm courses={data.courses}/>

</main>