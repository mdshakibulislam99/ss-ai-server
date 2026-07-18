<?php
/**
 * Health endpoint for the AI Server API.
 *
 * @package SS_AI_Image_Search
 * @subpackage Api
 */

declare( strict_types=1 );

namespace SS_AI_Image_Search\Api\Endpoints;

use SS_AI_Image_Search\Api\Client;
use SS_AI_Image_Search\Api\Response;
use SS_AI_Image_Search\Exceptions\Api\ApiException;

/**
 * Health endpoint class for health check operations.
 */
class HealthEndpoint {

	/**
	 * API Client instance.
	 *
	 * @var Client
	 */
	private Client $client;

	/**
	 * Constructor.
	 *
	 * @param Client $client API Client instance.
	 */
	public function __construct( Client $client ) {
		$this->client = $client;
	}

	/**
	 * Check server health.
	 *
	 * @return Response Response object.
	 * @throws ApiException If request fails.
	 */
	public function check(): Response {
		$endpoint = 'health';

		return $this->client->get( $endpoint );
	}

	/**
	 * Check server health with detailed information.
	 *
	 * @return Response Response object.
	 * @throws ApiException If request fails.
	 */
	public function check_detailed(): Response {
		$endpoint = 'health/detailed';

		return $this->client->get( $endpoint );
	}

	/**
	 * Check database health.
	 *
	 * @return Response Response object.
	 * @throws ApiException If request fails.
	 */
	public function check_database(): Response {
		$endpoint = 'health/database';

		return $this->client->get( $endpoint );
	}

	/**
	 * Check AI provider health.
	 *
	 * @return Response Response object.
	 * @throws ApiException If request fails.
	 */
	public function check_ai_provider(): Response {
		$endpoint = 'health/ai-provider';

		return $this->client->get( $endpoint );
	}

	/**
	 * Check vector store health.
	 *
	 * @return Response Response object.
	 * @throws ApiException If request fails.
	 */
	public function check_vector_store(): Response {
		$endpoint = 'health/vector-store';

		return $this->client->get( $endpoint );
	}

	/**
	 * Get server readiness status.
	 *
	 * @return Response Response object.
	 * @throws ApiException If request fails.
	 */
	public function get_readiness(): Response {
		$endpoint = 'health/ready';

		return $this->client->get( $endpoint );
	}

	/**
	 * Get server liveness status.
	 *
	 * @return Response Response object.
	 * @throws ApiException If request fails.
	 */
	public function get_liveness(): Response {
		$endpoint = 'health/live';

		return $this->client->get( $endpoint );
	}
}