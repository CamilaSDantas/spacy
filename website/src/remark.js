import Link from './components/link'
import Section, { Hr } from './components/section'
import { Table, Tr, Th, Tx, Td } from './components/table'
import { Pre, Code, InlineCode, TypeAnnotation } from './components/code'
import { Ol, Ul, Li } from './components/list'
import { H2, H3, H4, H5, P, Abbr, Help, Label } from './components/typography'
import Accordion from './components/accordion'
import Infobox from './components/infobox'
import Aside from './components/aside'
import Button from './components/button'
import Tag from './components/tag'
import Grid from './components/grid'
import { YouTube, SoundCloud, Iframe, Image, GoogleSheet } from './components/embed'
import Project from './widgets/project'
import { Integration, IntegrationLogo } from './widgets/integration.js'
import { Logos, Colors, Patterns } from './widgets/styleguide'
import Changelog from './widgets/changelog.js'
import Features from './widgets/features.js'
import Landing from './widgets/landing.js'
import Languages from './widgets/languages.js'
import QuickstartInstall from './widgets/quickstart-install.js'
import QuickstartTraining from './widgets/quickstart-training.js'
import QuickstartModels from './widgets/quickstart-models.js'

import Benchmarks from '../docs/usage/_benchmarks-models.mdx'
import Architecture101 from '../docs/usage/101/_architecture.mdx'
import LanguageData101 from '../docs/usage/101/_language-data.mdx'
import NER101 from '../docs/usage/101/_named-entities.mdx'
import Pipelines101 from '../docs/usage/101/_pipelines.mdx'
import PosDeps101 from '../docs/usage/101/_pos-deps.mdx'
import Serialization101 from '../docs/usage/101/_serialization.mdx'
import Tokenization101 from '../docs/usage/101/_tokenization.mdx'
import Training101 from '../docs/usage/101/_training.mdx'
import Vectors101 from '../docs/usage/101/_vectors-similarity.mdx'

export const remarkComponents = {
    a: Link,
    p: P,
    pre: Pre,
    code: Code,
    inlineCode: InlineCode,
    del: TypeAnnotation,
    table: Table,
    img: Image,
    tr: Tr,
    th: Th,
    td: Td,
    ol: Ol,
    ul: Ul,
    li: Li,
    h2: H2,
    h3: H3,
    h4: H4,
    h5: H5,
    blockquote: Aside,
    section: Section,
    wrapper: ({ children }) => children,
    hr: Hr,

    Infobox,
    Table,
    Tr,
    Tx,
    Th,
    Td,
    Help,
    Button,
    YouTube,
    SoundCloud,
    Iframe,
    GoogleSheet,
    Abbr,
    Tag,
    Accordion,
    Grid,
    InlineCode,
    Project,
    Integration,
    IntegrationLogo,

    Label,
    Logos,
    Colors,
    Patterns,

    Changelog,
    Features,
    Landing,
    Languages,
    QuickstartInstall,
    QuickstartTraining,
    QuickstartModels,

    Benchmarks,
    Architecture101,
    LanguageData101,
    NER101,
    Pipelines101,
    PosDeps101,
    Serialization101,
    Tokenization101,
    Training101,
    Vectors101,
}