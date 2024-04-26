/**
 * Bundled by jsDelivr using Rollup v2.79.1 and Terser v5.19.2.
 * Original file: /npm/@google/generative-ai@0.7.1/dist/index.mjs
 *
 * Do NOT use SRI with dynamically generated files! More information: https://www.jsdelivr.com/using-sri-with-dynamic-files
 */
/**
 * @license
 * Copyright 2024 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
const t=["user","model","function","system"];var n,e,s,o,i,a,r,c;!function(t){t.HARM_CATEGORY_UNSPECIFIED="HARM_CATEGORY_UNSPECIFIED",t.HARM_CATEGORY_HATE_SPEECH="HARM_CATEGORY_HATE_SPEECH",t.HARM_CATEGORY_SEXUALLY_EXPLICIT="HARM_CATEGORY_SEXUALLY_EXPLICIT",t.HARM_CATEGORY_HARASSMENT="HARM_CATEGORY_HARASSMENT",t.HARM_CATEGORY_DANGEROUS_CONTENT="HARM_CATEGORY_DANGEROUS_CONTENT"}(n||(n={})),function(t){t.HARM_BLOCK_THRESHOLD_UNSPECIFIED="HARM_BLOCK_THRESHOLD_UNSPECIFIED",t.BLOCK_LOW_AND_ABOVE="BLOCK_LOW_AND_ABOVE",t.BLOCK_MEDIUM_AND_ABOVE="BLOCK_MEDIUM_AND_ABOVE",t.BLOCK_ONLY_HIGH="BLOCK_ONLY_HIGH",t.BLOCK_NONE="BLOCK_NONE"}(e||(e={})),function(t){t.HARM_PROBABILITY_UNSPECIFIED="HARM_PROBABILITY_UNSPECIFIED",t.NEGLIGIBLE="NEGLIGIBLE",t.LOW="LOW",t.MEDIUM="MEDIUM",t.HIGH="HIGH"}(s||(s={})),function(t){t.BLOCKED_REASON_UNSPECIFIED="BLOCKED_REASON_UNSPECIFIED",t.SAFETY="SAFETY",t.OTHER="OTHER"}(o||(o={})),function(t){t.FINISH_REASON_UNSPECIFIED="FINISH_REASON_UNSPECIFIED",t.STOP="STOP",t.MAX_TOKENS="MAX_TOKENS",t.SAFETY="SAFETY",t.RECITATION="RECITATION",t.OTHER="OTHER"}(i||(i={})),function(t){t.TASK_TYPE_UNSPECIFIED="TASK_TYPE_UNSPECIFIED",t.RETRIEVAL_QUERY="RETRIEVAL_QUERY",t.RETRIEVAL_DOCUMENT="RETRIEVAL_DOCUMENT",t.SEMANTIC_SIMILARITY="SEMANTIC_SIMILARITY",t.CLASSIFICATION="CLASSIFICATION",t.CLUSTERING="CLUSTERING"}(a||(a={})),function(t){t.MODE_UNSPECIFIED="MODE_UNSPECIFIED",t.AUTO="AUTO",t.ANY="ANY",t.NONE="NONE"}(r||(r={})),function(t){t.STRING="STRING",t.NUMBER="NUMBER",t.INTEGER="INTEGER",t.BOOLEAN="BOOLEAN",t.ARRAY="ARRAY",t.OBJECT="OBJECT"}(c||(c={}));
/**
 * @license
 * Copyright 2024 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
class d extends Error{constructor(t){super(`[GoogleGenerativeAI Error]: ${t}`)}}class l extends d{constructor(t,n){super(t),this.response=n}}
/**
 * @license
 * Copyright 2024 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */const u="0.7.1",h="genai-js";var f;!function(t){t.GENERATE_CONTENT="generateContent",t.STREAM_GENERATE_CONTENT="streamGenerateContent",t.COUNT_TOKENS="countTokens",t.EMBED_CONTENT="embedContent",t.BATCH_EMBED_CONTENTS="batchEmbedContents"}(f||(f={}));class E{constructor(t,n,e,s,o){this.model=t,this.task=n,this.apiKey=e,this.stream=s,this.requestOptions=o}toString(){var t,n;const e=(null===(t=this.requestOptions)||void 0===t?void 0:t.apiVersion)||"v1beta";let s=`${(null===(n=this.requestOptions)||void 0===n?void 0:n.baseUrl)||"https://us-central1-ganai-apac.cloudfunctions.net/gemini"}/${e}/${this.model}:${this.task}`;return this.stream&&(s+="?alt=sse"),s}}async function p(t){const n=new Headers;return n.append("Content-Type","application/json"),n.append("x-goog-api-client",function(t){const n=[];return(null==t?void 0:t.apiClient)&&n.push(t.apiClient),n.push(`${h}/${u}`),n.join(" ")}(t.requestOptions)),n.append("x-goog-api-key",t.apiKey),n}async function g(t,n,e,s,o,i){return async function(t,n,e,s,o,i,a=fetch){const r=new E(t,n,e,s,i);let c;try{const r=await async function(t,n,e,s,o,i){const a=new E(t,n,e,s,i);return{url:a.toString(),fetchOptions:Object.assign(Object.assign({},O(i)),{method:"POST",headers:await p(a),body:o})}}(t,n,e,s,o,i);if(c=await a(r.url,r.fetchOptions),!c.ok){let t="";try{const n=await c.json();t=n.error.message,n.error.details&&(t+=` ${JSON.stringify(n.error.details)}`)}catch(t){}throw new Error(`[${c.status} ${c.statusText}] ${t}`)}}catch(t){const n=new d(`Error fetching from ${r.toString()}: ${t.message}`);throw n.stack=t.stack,n}return c}(t,n,e,s,o,i,fetch)}function O(t){const n={};if((null==t?void 0:t.timeout)>=0){const e=new AbortController,s=e.signal;setTimeout((()=>e.abort()),t.timeout),n.signal=s}return n}
/**
 * @license
 * Copyright 2024 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function C(t){return t.text=()=>{if(t.candidates&&t.candidates.length>0){if(t.candidates.length>1&&console.warn(`This response had ${t.candidates.length} candidates. Returning text from the first candidate only. Access response.candidates directly to use the other candidates.`),_(t.candidates[0]))throw new l(`${T(t)}`,t);return function(t){var n,e,s,o;return(null===(o=null===(s=null===(e=null===(n=t.candidates)||void 0===n?void 0:n[0].content)||void 0===e?void 0:e.parts)||void 0===s?void 0:s[0])||void 0===o?void 0:o.text)?t.candidates[0].content.parts.map((({text:t})=>t)).join(""):""}(t)}if(t.promptFeedback)throw new l(`Text not available. ${T(t)}`,t);return""},t.functionCall=()=>{if(t.candidates&&t.candidates.length>0){if(t.candidates.length>1&&console.warn(`This response had ${t.candidates.length} candidates. Returning function calls from the first candidate only. Access response.candidates directly to use the other candidates.`),_(t.candidates[0]))throw new l(`${T(t)}`,t);return console.warn("response.functionCall() is deprecated. Use response.functionCalls() instead."),m(t)[0]}if(t.promptFeedback)throw new l(`Function call not available. ${T(t)}`,t)},t.functionCalls=()=>{if(t.candidates&&t.candidates.length>0){if(t.candidates.length>1&&console.warn(`This response had ${t.candidates.length} candidates. Returning function calls from the first candidate only. Access response.candidates directly to use the other candidates.`),_(t.candidates[0]))throw new l(`${T(t)}`,t);return m(t)}if(t.promptFeedback)throw new l(`Function call not available. ${T(t)}`,t)},t}function m(t){var n,e,s,o;const i=[];if(null===(e=null===(n=t.candidates)||void 0===n?void 0:n[0].content)||void 0===e?void 0:e.parts)for(const n of null===(o=null===(s=t.candidates)||void 0===s?void 0:s[0].content)||void 0===o?void 0:o.parts)n.functionCall&&i.push(n.functionCall);return i.length>0?i:void 0}const y=[i.RECITATION,i.SAFETY];function _(t){return!!t.finishReason&&y.includes(t.finishReason)}function T(t){var n,e,s;let o="";if(t.candidates&&0!==t.candidates.length||!t.promptFeedback){if(null===(s=t.candidates)||void 0===s?void 0:s[0]){const n=t.candidates[0];_(n)&&(o+=`Candidate was blocked due to ${n.finishReason}`,n.finishMessage&&(o+=`: ${n.finishMessage}`))}}else o+="Response was blocked",(null===(n=t.promptFeedback)||void 0===n?void 0:n.blockReason)&&(o+=` due to ${t.promptFeedback.blockReason}`),(null===(e=t.promptFeedback)||void 0===e?void 0:e.blockReasonMessage)&&(o+=`: ${t.promptFeedback.blockReasonMessage}`);return o}function N(t){return this instanceof N?(this.v=t,this):new N(t)}function I(t,n,e){if(!Symbol.asyncIterator)throw new TypeError("Symbol.asyncIterator is not defined.");var s,o=e.apply(t,n||[]),i=[];return s={},a("next"),a("throw"),a("return"),s[Symbol.asyncIterator]=function(){return this},s;function a(t){o[t]&&(s[t]=function(n){return new Promise((function(e,s){i.push([t,n,e,s])>1||r(t,n)}))})}function r(t,n){try{(e=o[t](n)).value instanceof N?Promise.resolve(e.value.v).then(c,d):l(i[0][2],e)}catch(t){l(i[0][3],t)}var e}function c(t){r("next",t)}function d(t){r("throw",t)}function l(t,n){t(n),i.shift(),i.length&&r(i[0][0],i[0][1])}}"function"==typeof SuppressedError&&SuppressedError;
/**
 * @license
 * Copyright 2024 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
const R=/^data\: (.*)(?:\n\n|\r\r|\r\n\r\n)/;function A(t){const n=function(t){const n=t.getReader();return new ReadableStream({start(t){let e="";return s();function s(){return n.read().then((({value:n,done:o})=>{if(o)return e.trim()?void t.error(new d("Failed to parse stream")):void t.close();e+=n;let i,a=e.match(R);for(;a;){try{i=JSON.parse(a[1])}catch(n){return void t.error(new d(`Error parsing JSON response: "${a[1]}"`))}t.enqueue(i),e=e.substring(a[0].length),a=e.match(R)}return s()}))}}})}(t.body.pipeThrough(new TextDecoderStream("utf8",{fatal:!0}))),[e,s]=n.tee();return{stream:v(e),response:S(s)}}async function S(t){const n=[],e=t.getReader();for(;;){const{done:t,value:s}=await e.read();if(t)return C(w(n));n.push(s)}}function v(t){return I(this,arguments,(function*(){const n=t.getReader();for(;;){const{value:t,done:e}=yield N(n.read());if(e)break;yield yield N(C(t))}}))}function w(t){const n=t[t.length-1],e={promptFeedback:null==n?void 0:n.promptFeedback};for(const n of t)if(n.candidates)for(const t of n.candidates){const n=t.index;if(e.candidates||(e.candidates=[]),e.candidates[n]||(e.candidates[n]={index:t.index}),e.candidates[n].citationMetadata=t.citationMetadata,e.candidates[n].finishReason=t.finishReason,e.candidates[n].finishMessage=t.finishMessage,e.candidates[n].safetyRatings=t.safetyRatings,t.content&&t.content.parts){e.candidates[n].content||(e.candidates[n].content={role:t.content.role||"user",parts:[]});const s={};for(const o of t.content.parts)o.text&&(s.text=o.text),o.functionCall&&(s.functionCall=o.functionCall),0===Object.keys(s).length&&(s.text=""),e.candidates[n].content.parts.push(s)}}return e}
/**
 * @license
 * Copyright 2024 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */async function M(t,n,e,s){return A(await g(n,f.STREAM_GENERATE_CONTENT,t,!0,JSON.stringify(e),s))}async function b(t,n,e,s){const o=await g(n,f.GENERATE_CONTENT,t,!1,JSON.stringify(e),s);return{response:C(await o.json())}}
/**
 * @license
 * Copyright 2024 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */function L(t){let n=[];if("string"==typeof t)n=[{text:t}];else for(const e of t)"string"==typeof e?n.push({text:e}):n.push(e);return function(t){const n={role:"user",parts:[]},e={role:"function",parts:[]};let s=!1,o=!1;for(const i of t)"functionResponse"in i?(e.parts.push(i),o=!0):(n.parts.push(i),s=!0);if(s&&o)throw new d("Within a single message, FunctionResponse cannot be mixed with other type of part in the request for sending chat message.");if(!s&&!o)throw new d("No content is provided for sending chat message.");if(s)return n;return e}(n)}function H(t){if(t.contents)return t;return{contents:[L(t)]}}
/**
 * @license
 * Copyright 2024 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
const D=["text","inlineData","functionCall","functionResponse"],F={user:["text","inlineData"],function:["functionResponse"],model:["text","functionCall"],system:["text"]},P={user:["model"],function:["model"],model:["user","function"],system:[]};
/**
 * @license
 * Copyright 2024 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
const $="SILENT_ERROR";class G{constructor(n,e,s,o){this.model=e,this.params=s,this.requestOptions=o,this._history=[],this._sendPromise=Promise.resolve(),this._apiKey=n,(null==s?void 0:s.history)&&(!function(n){let e;for(const s of n){const{role:n,parts:o}=s;if(!e&&"user"!==n)throw new d(`First content should be with role 'user', got ${n}`);if(!t.includes(n))throw new d(`Each item should include role field. Got ${n} but valid roles are: ${JSON.stringify(t)}`);if(!Array.isArray(o))throw new d("Content should have 'parts' property with an array of Parts");if(0===o.length)throw new d("Each Content should have at least one part");const i={text:0,inlineData:0,functionCall:0,functionResponse:0};for(const t of o)for(const n of D)n in t&&(i[n]+=1);const a=F[n];for(const t of D)if(!a.includes(t)&&i[t]>0)throw new d(`Content with role '${n}' can't contain '${t}' part`);if(e&&!P[n].includes(e.role))throw new d(`Content with role '${n}' can't follow '${e.role}'. Valid previous roles: ${JSON.stringify(P)}`);e=s}}(s.history),this._history=s.history)}async getHistory(){return await this._sendPromise,this._history}async sendMessage(t){var n,e,s,o,i;await this._sendPromise;const a=L(t),r={safetySettings:null===(n=this.params)||void 0===n?void 0:n.safetySettings,generationConfig:null===(e=this.params)||void 0===e?void 0:e.generationConfig,tools:null===(s=this.params)||void 0===s?void 0:s.tools,toolConfig:null===(o=this.params)||void 0===o?void 0:o.toolConfig,systemInstruction:null===(i=this.params)||void 0===i?void 0:i.systemInstruction,contents:[...this._history,a]};let c;return this._sendPromise=this._sendPromise.then((()=>b(this._apiKey,this.model,r,this.requestOptions))).then((t=>{var n;if(t.response.candidates&&t.response.candidates.length>0){this._history.push(a);const e=Object.assign({parts:[],role:"model"},null===(n=t.response.candidates)||void 0===n?void 0:n[0].content);this._history.push(e)}else{const n=T(t.response);n&&console.warn(`sendMessage() was unsuccessful. ${n}. Inspect response object for details.`)}c=t})),await this._sendPromise,c}async sendMessageStream(t){var n,e,s,o,i;await this._sendPromise;const a=L(t),r={safetySettings:null===(n=this.params)||void 0===n?void 0:n.safetySettings,generationConfig:null===(e=this.params)||void 0===e?void 0:e.generationConfig,tools:null===(s=this.params)||void 0===s?void 0:s.tools,toolConfig:null===(o=this.params)||void 0===o?void 0:o.toolConfig,systemInstruction:null===(i=this.params)||void 0===i?void 0:i.systemInstruction,contents:[...this._history,a]},c=M(this._apiKey,this.model,r,this.requestOptions);return this._sendPromise=this._sendPromise.then((()=>c)).catch((t=>{throw new Error($)})).then((t=>t.response)).then((t=>{if(t.candidates&&t.candidates.length>0){this._history.push(a);const n=Object.assign({},t.candidates[0].content);n.role||(n.role="model"),this._history.push(n)}else{const n=T(t);n&&console.warn(`sendMessageStream() was unsuccessful. ${n}. Inspect response object for details.`)}})).catch((t=>{t.message!==$&&console.error(t)})),c}}
/**
 * @license
 * Copyright 2024 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
/**
 * @license
 * Copyright 2024 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
class U{constructor(t,n,e){this.apiKey=t,n.model.includes("/")?this.model=n.model:this.model=`models/${n.model}`,this.generationConfig=n.generationConfig||{},this.safetySettings=n.safetySettings||[],this.tools=n.tools,this.toolConfig=n.toolConfig,this.systemInstruction=n.systemInstruction,this.requestOptions=e||{}}async generateContent(t){const n=H(t);return b(this.apiKey,this.model,Object.assign({generationConfig:this.generationConfig,safetySettings:this.safetySettings,tools:this.tools,toolConfig:this.toolConfig,systemInstruction:this.systemInstruction},n),this.requestOptions)}async generateContentStream(t){const n=H(t);return M(this.apiKey,this.model,Object.assign({generationConfig:this.generationConfig,safetySettings:this.safetySettings,tools:this.tools,toolConfig:this.toolConfig,systemInstruction:this.systemInstruction},n),this.requestOptions)}startChat(t){return new G(this.apiKey,this.model,Object.assign({generationConfig:this.generationConfig,safetySettings:this.safetySettings,tools:this.tools,toolConfig:this.toolConfig,systemInstruction:this.systemInstruction},t),this.requestOptions)}async countTokens(t){const n=H(t);return async function(t,n,e,s){return(await g(n,f.COUNT_TOKENS,t,!1,JSON.stringify(Object.assign(Object.assign({},e),{model:n})),s)).json()}
/**
 * @license
 * Copyright 2024 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */(this.apiKey,this.model,n,this.requestOptions)}async embedContent(t){const n=function(t){if("string"==typeof t||Array.isArray(t))return{content:L(t)};return t}(t);return async function(t,n,e,s){return(await g(n,f.EMBED_CONTENT,t,!1,JSON.stringify(e),s)).json()}(this.apiKey,this.model,n,this.requestOptions)}async batchEmbedContents(t){return async function(t,n,e,s){const o=e.requests.map((t=>Object.assign(Object.assign({},t),{model:n})));return(await g(n,f.BATCH_EMBED_CONTENTS,t,!1,JSON.stringify({requests:o}),s)).json()}(this.apiKey,this.model,t,this.requestOptions)}}
/**
 * @license
 * Copyright 2024 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */class B{constructor(t){this.apiKey=t}getGenerativeModel(t,n){if(!t.model)throw new d("Must provide a model name. Example: genai.getGenerativeModel({ model: 'my-model-name' })");return new U(this.apiKey,t,n)}}export{o as BlockReason,G as ChatSession,i as FinishReason,r as FunctionCallingMode,c as FunctionDeclarationSchemaType,U as GenerativeModel,B as GoogleGenerativeAI,e as HarmBlockThreshold,n as HarmCategory,s as HarmProbability,t as POSSIBLE_ROLES,a as TaskType};export default null;
//# sourceMappingURL=/sm/f6bbdf2725c3e9ecd3fc091561b12f62901cfacab55247adb8821d94dcea4a95.map