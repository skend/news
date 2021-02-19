import Head from 'next/head'
import Link from 'next/link'
import styles from '../styles/Home.module.css'
import Header from '../components/Header/Header'
import Footer from '../components/Footer/Footer'

export async function getServerSideProps() {

  const res = await fetch(`http://127.0.0.1:5000/search`,
    { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(
      {"filter":{"source":"ft","title":{"$regex":""}},"skip":0,"limit":30}
    )}
  )

  const data = await res.json()
  return { props: { data } }
}

function Home({ data }) {
  return (
    <div className={styles.container}>
      <Head>
        <title>News | Home</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <Header/>

        <div className={styles.grid}>

          {data.map((value, index) => {
            return <Link href={value.url} key={value._id}>
                <a className={styles.card}>
                  <h3>{value.title}</h3>
                  <p>{value.description}</p>
                </a>
              </Link>
          })}

        </div>
      </main>

      <Footer/>
    </div>
  )
}

export default Home
