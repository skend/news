const searchDb = async event => {
    event.preventDefault();
    console.log(event)
}

export default function Search() {
    return <div>
    <form onSubmit={searchDb}>
        <input id="search-box" name="name" type="text" />
        <button type="submit" onKeyDown={(e) => something(e) }>search</button>
    </form>
    </div>
}