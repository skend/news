import Head from 'next/head'
import Link from 'next/link'
import styles from '../styles/Home.module.css'

// This gets called on every request
export async function getServerSideProps() {
  // Fetch data from external API
  const res = await fetch(`http://127.0.0.1:5000/search`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({"source": "ft"})})
  const data = await res.json()

  // Pass data to the page via props
  return { props: { data } }
}

function Home({ data }) {
  console.log(data)
  return (
    <div className={styles.container}>
      <Head>
        <title>News | Home</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>
          Welcome to <a href="https://nextjs.org">&lt;insert name here&gt;</a>
        </h1>

        <div className={styles.grid}>

          {data.map((value, index) => {
            return <Link href={value.link}>
                <a className={styles.card}>
                  <h3>{value.title}</h3>
                  <p>{value.description}</p>
                </a>
              </Link>
          })}

        </div>
      </main>

      <footer className={styles.footer}>
        <a
          href="https://vercel.com?utm_source=create-next-app&utm_medium=default-template&utm_campaign=create-next-app"
          target="_blank"
          rel="noopener noreferrer"
        >
          Created by&nbsp;{" "}
          <Link href="https://github.com/skend">
            <a className={styles.github}>skend</a>
          </Link>
        </a>
      </footer>
    </div>
  )
}

export default Home
