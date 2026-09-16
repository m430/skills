---
name: setup-ts-deep-modules
description: 把 dependency-cruiser 接入 TypeScript 仓库，让每个包都是一个深模块（deep module），实现隐藏在子文件夹中，只能通过其入口文件触达。用户调用。
disable-model-invocation: true
---

# 配置 TS 深模块

让本仓库中的每个包都成为一个**深模块（deep module）**：小接口背后藏着大量行为。包的公共表面是它的**入口点（entry point）**（包根目录下的那些文件），其子文件夹中的一切都是隐藏的。本技能会安装 [dependency-cruiser](https://github.com/sverweij/dependency-cruiser) 以及让入口点成为唯一进入方式的规则，然后证明这些规则真的会咬人。

词汇方面（深模块、接口、接缝（seam）、深度），调用 Skill 工具并传入 "codebase-design"，并全程沿用它的语言。

## 它强制约束的形态

```
src/packages/
  <name>/
    index.ts        ← an entry point (public). Import this from outside.
    client.ts       ← another entry point. Packages may expose SEVERAL.
    lib/            ← implementation: hidden from outside, free to import each other.
    tests/          ← co-located tests + fixtures (a subfolder, so private).
```

公共表面是包的**根文件**，而不是某个指定的 `index.ts`。按惯例，实现放在 `lib/`，测试放在 `tests/`，这让每个包都具有同样的双文件夹形态。但规则本身是一般性的：*任何*子文件夹中的*任何*东西都是私有的，所以你永远不需要为了新增文件夹而扩展配置。

四条规则，全部为 `error`：

1. **入口点边界**：包外的代码（应用代码或其他包）只能 import 该包的入口点（它的根文件），绝不能 import 它子文件夹里的任何东西。
2. **包内自由**：包自己的文件之间可以自由 import。
3. **测试经由入口点**：`<pkg>/tests/` 下的文件可以 import 任何包的入口点以及自己 `tests/` 里的 fixture，但绝不能 import 任何包的子文件夹内部（连它们自己的也不行）。跨包的集成测试没问题；深层 import 不行。
4. **禁止循环**：不允许出现依赖循环。

**入口点，而不是 barrel。**因为公共表面是*每一个*根文件，一个包可以暴露多个小入口点（`index.ts`、`client.ts`、`server.ts`），而不必把所有东西都汇入一个巨大的 `index.ts`。把整棵子树重新导出的 barrel 文件不推荐使用；保持入口点小，把实现藏进子文件夹。

分层（哪些包可以依赖哪些包）是*另一回事*，在配置中留作一个带注释的桩，由本仓库自行填写。

## 步骤

### 1. 探测环境

- **包管理器**：`pnpm-lock.yaml` → pnpm，`yarn.lock` → yarn，`bun.lockb` → bun，否则 npm。下方的每条命令都用它（`pnpm`/`yarn`/`npm run`/`bunx`）。
- **包根目录**：如果 `src/` 存在就用 `src/packages`，否则用 `packages`。如果仓库已经有明显不同的约定，与用户确认这个选择。
- **现有配置**：检查是否存在 `.dependency-cruiser.*` 文件。如果存在，**不要**覆盖它：把四条规则和选项合并进去，并告诉用户你添加了什么。

**完成条件：**包管理器、包根目录和现有配置状态都已确定。

### 2. 安装 dependency-cruiser

用探测到的包管理器把 `dependency-cruiser` 安装为 devDependency。

**完成条件：**`dependency-cruiser` 出现在 `devDependencies` 中。

### 3. 写配置

把 [`dependency-cruiser.config.cjs`](./dependency-cruiser.config.cjs) 复制到仓库根目录，命名为 `.dependency-cruiser.cjs`。把 `PACKAGES_ROOT` 设为第 1 步探测到的根目录。这些规则基于路径深度且与扩展名无关，所以其他内容不需要调整。

**完成条件：**`.dependency-cruiser.cjs` 已存在且 `PACKAGES_ROOT` 正确，并且四条禁止性规则都在。

### 4. 接入检查

- 添加一个 `lint:boundaries` 脚本：`depcruise <packages-root>`（或 `depcruise src`）。
- 把它并入仓库的总检查命令，也就是已经在跑 typecheck 的那条（例如 `check` / `ci` / `validate` 脚本）。**不要**动 `tsconfig`，也不要添加路径别名。
- 如果没有总检查脚本，就添加 `lint:boundaries`，并告诉用户把它纳入 CI。

**完成条件：**`lint:boundaries` 已存在，并且作为 typecheck 所在的同一条命令的一部分运行。

### 5. 搭建示例包

创建一个提交入库的 `<packages-root>/example/` 作为照抄模板：

- `index.ts` 是一个入口点。导出一个委托给内部文件的函数（这样这个包看起来就是*深的*，而不是一层透传）。
- `lib/impl.ts`：**子文件夹**中的一个内部文件，由 `index.ts` import，外部无法触达。
- `tests/example.test.ts` **只** import `../index`（一个入口点），并针对公共函数做断言。

告诉用户这是一个可以照抄或删除的起步模板。

**完成条件：**示例包已存在，通过根目录入口点暴露其行为，并把 `impl` 藏在子文件夹中。

### 6. 证明规则真的会咬人

这是整个技能的完成标准：一个在违规时不报错的配置毫无价值。

1. 运行 `lint:boundaries`。它在干净的示例上必须**通过**。
2. 临时向 `tests/example.test.ts` 添加一个深层 import（例如 `import { thing } from "../lib/impl"`）。再次运行 `lint:boundaries`；它必须**失败**并报 `tests-through-entrypoints`。
3. 撤销那个深层 import。再运行一次，必须**通过**。

**完成条件：**你已经观察到先通过、然后因深层 import 而失败、然后再次通过。如果第 2 步没有失败，说明规则没有接对，先修复再收尾。

### 7. 把约定写成文档

在**包文件夹里**写一个 `README.md`（`<packages-root>/README.md`，与它所管辖的包放在一起），内容涵盖：`src/packages/<name>/` 布局（入口点在根目录，`lib/` 放实现，`tests/` 放测试）、"只能通过包的入口点（它的根文件）来 import"，以及如何运行 `lint:boundaries`。**明确不推荐 barrel 文件**：暴露多个小入口点，而不是通过一个 index 重新导出整棵子树。篇幅控制在照抄片段加四条规则、每条规则一段。

然后从仓库的代理指令文件（有 `CLAUDE.md` 就用它，否则用 `AGENTS.md`，两者都没有就创建 `AGENTS.md`）向它添加一个**上下文指针（context pointer）**。一行就够，例如 `Packages are deep modules: see [src/packages/README.md](./src/packages/README.md) before adding or importing one.`。有了它，代理才会发现边界规则，而不是被它绊倒。

**完成条件：**`<packages-root>/README.md` 已存在且不推荐 barrel，并且仓库的 `CLAUDE.md`/`AGENTS.md` 链接到它。

## 备注

- 配置里的 `$1` 反向引用（dependency-cruiser 的分组匹配）正是让包能触达自身内部、而外部不能的关键。不要把它们摊平成一条条单独的按包规则。
- 公有还是私有由**深度**决定：包的根文件是入口点；子文件夹里的一切都是私有的。惯例的子文件夹是 `lib/`（实现）和 `tests/`，但规则并没有把它们写死：任何子文件夹都是私有的，所以新增文件夹永远不需要改配置。添加入口点就是添加一个根文件（不要 barrel）。
- 包是**扁平的**：根目录下只有一层直接子项。包的内部想嵌套多深都可以；但一个包不能包含另一个包。
- 使用 `.cjs`（而不是 `.js`），这样配置的 `module.exports` 即使在 `"type": "module"` 仓库里也能工作。
