# HTML structure

The special difficulty is parsing different etymologies.

The structure of a page with only one etymology is as follows:
```
<body>
<section (empty, uninteresting)/>
<section that we are interested int>
    <h1 id="Русский">
    <maybe useless table linking to wikipedia>
    <section>
        <h3 id="Морфологические и синтаксические свойства">
        <table class="morfotable-ru">
        <p with grammatical info>
    <section with pronounciation>
        <h3 id="Произношение">
    <section with definition>
        <h3 id="Семантические_свойства">
        <section>
            <h4 id = "Значение">
</section>
</body>
```

For two etymologies, it is like this:

```
<body>
<section (empty, uninteresting)/>
<section that we are interested int>
    <h1 id="Русский">
    <section for etymology 1>
        <h2 id=опрвка 1>
        <section>
            <h3 id="Морфологические и синтаксические свойства">
            <table class="morfotable-ru">
            <p with grammatical info>
        <section with pronounciation>
            <h3 id="Произношение">
        <section with definition>
        <h3 id="Семантические_свойства">
        <section>
            <h4 id = "Значение">
    </section for etymology 1>
    <section for etymology 2>
</section>
</body>

```