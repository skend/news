import Link from 'next/link'
import styles from './Header.module.css'

export default function Header() {
    return <div className={styles.header}>
        <h1 className={styles.title}>
        <Link href="https://nextjs.org">
            <a>&lt;insert name here&gt;</a>
        </Link>
        </h1>

        {/* <div className={styles.searchBar}>

        </div> */}
    </div>
}